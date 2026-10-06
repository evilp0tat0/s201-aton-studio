#!/usr/bin/env python3
"""source_scan.py — the one lexer that tells comments from code in s201_aton_studio.html.

Two tools need to know exactly where the app's comments are:
  * build-end-user-version.py strips every comment out of the tester bundle (strip_comments below);
  * code_notes.py (pre-commit check #22, foundational Rule 26) finds the lines of code that carry no note.
Both read the file through this module, so the two can never disagree about what is a comment (Rule 23).

A real JavaScript parser cannot be used: the file uses ES2020 syntax (optional chaining) that the Python parsers
available here do not read, and no dependency is added for it. The lexer below knows just enough JavaScript to never
mistake a string, a template literal or a regular expression for a comment — a URL such as "http://…" inside a string,
or the `//` of a pattern, stays code. Its correctness is proven the hard way: the end-user bundle is built with it and
the app's whole self-test suite then passes on that comment-free copy; pre-commit check #22 also compiles the script
with a mark written inside every comment and literal the lexer found, which fails wherever the lexer and V8 disagree.

Each stripper returns the text without its comments (run()) and records, in `comments`, the (start, end) offsets of
every comment it removed, in the coordinates of the text it was given. JSStripper also records, in `literals`, the
(start, end) offsets of every string and regular expression and of each text piece of a template literal (the code of a
template's ${…} is code, so it is in no piece), so the lines of a literal that runs over several lines can be told from
code; HtmlCssStripper records, in `css_regions`, the (start, end) offsets of the CSS inside each <style> element, so
markup and CSS can be told apart.
"""

# The markers of the app's one inline script: the whole JavaScript sits between the first of each.
OPEN = "<script>"
CLOSE = "</script>"

# Keywords after which a "/" starts a regular expression, not a division (e.g. `return /x/.test(s)`).
REGEX_PRECEDING_KEYWORDS = {
    "return", "typeof", "instanceof", "in", "of", "new", "delete", "void",
    "do", "else", "yield", "await", "throw", "case", "default",
}
# Keywords whose parenthesised head may be followed by a statement that starts with a regular expression
# (`if (x) /re/.test(s)`); after any other closing parenthesis — a call's, a group's — a "/" divides.
REGEX_AFTER_PAREN_KEYWORDS = {"if", "while", "for", "with"}
# The characters that end a line for JavaScript (ECMAScript LineTerminator: LF, CR, U+2028, U+2029): a "//" comment and
# a regular expression stop at any of them, as V8 stops them, so code after one is never taken for part of a comment.
LINE_TERMINATORS = "\n\r\u2028\u2029"


def _preceding_ws_count(out):
    """How many spaces or tabs end the output since its last line break — or -1 when anything else stands there.

    A comment that is alone on its line is removed together with its indentation (and its line break); a comment after
    code on the same line keeps the code's spacing. This count tells the two apart."""
    cnt = 0
    k = len(out) - 1
    # walk back over the output pieces written so far, one character each at the line's end
    while k >= 0:
        ch = out[k]
        # reached the previous line: everything before the comment on this line was indentation
        if ch == "\n":
            break
        # indentation: count it and keep walking back
        if ch == " " or ch == "\t":
            cnt += 1
            k -= 1
            continue
        # code stands before the comment on this line
        return -1
    return cnt


def _drop_comment_line(out, s, n, after, pw):
    """Where to resume after a block comment that ended at `after`, and what to write for it.

    A comment alone on its line(s) — only indentation before it (pw >= 0) and nothing but spaces after it — is removed
    with its indentation and its line break, so no blank line is left; any other comment is replaced by one space, so
    the tokens on either side stay apart. Returns (resume offset, text to write)."""
    k = after
    # skip the spaces after the comment to see whether the line ends there
    while k < n and s[k] in " \t":
        k += 1
    line_ends = (k >= n or s[k] == "\n")
    # alone on its line: drop the indentation already written, and the line break after the comment
    if pw >= 0 and line_ends:
        for _ in range(pw):
            out.pop()
        return ((k + 1) if (k < n and s[k] == "\n") else k), ""
    # after or before code on the same line: one space keeps the tokens apart
    return after, " "


class JSStripper:
    """Removes the comments from JavaScript source, and records where each one was.

    It walks the text once, character by character, and knows the places where "/" or a quote does NOT start a comment:
    strings ('…', "…"), template literals (`…${…}…`, whose ${…} are code again) and regular-expression literals. Whether a
    "/" begins a regular expression or a division is decided by what came before it (self.prev), as a JavaScript parser
    does: after an operator, an opening brace, a closing brace, a keyword such as `return`, or the parenthesised head of
    `if`, `while`, `for` or `with`, it is a regular expression; after a name, a number, or any other closing parenthesis
    or bracket it is a division. The comments it knows are V8's in a classic script: `//` and `/* */`, and the HTML-like
    `<!--` anywhere and `-->` at a line's start, each running to the line's end."""

    # the lexer's state: the text and where it reads, what it has written, the last token, and the spans it found
    def __init__(self, s):
        # one pass over the text: the read position `i` only moves forward, so the lexer is linear in the file's size
        self.s = s
        self.i = 0
        self.n = len(s)
        # the stripped text, built piece by piece
        self.out = []
        # the kind of the last significant token: "" (start), "op", "rbrace", "kw_expr", "kw_paren", "ident", "num",
        # "str", "regex", "rparen", "rbracket" — what decides whether the next "/" starts a regular expression; the last
        # name read, and for each open parenthesis whether it follows `if`, `while`, `for` or `with`
        self.prev = ""
        self.last_word = ""
        self.parens = []
        # (start, end) of every comment removed, and of every string, regular expression and template text piece, in
        # the coordinates of `s`; for each template text piece, by its start, where its whole template ends (a line of
        # template text belongs to the template until the template closes, fields and all)
        self.comments = []
        self.literals = []
        self.literal_ends = {}

    def run(self):
        """The source without its comments (self.comments holds where they were)."""
        self._scan_code(top=True)
        return "".join(self.out)

    def _regex_allowed(self):
        """Whether a "/" here starts a regular expression: after an operator, a closing brace, an expression keyword or a
        keyword's parenthesised head."""
        return self.prev in ("", "op", "rbrace", "kw_expr", "kw_paren")

    def _scan_string(self, quote):
        """Copy a '…' or "…" string whole, backslash escapes included, so nothing in it is read as code."""
        s, n, out = self.s, self.n, self.out
        out.append(quote)
        i = self.i + 1
        # up to and including the closing quote
        while i < n:
            c = s[i]
            # an escape: copy the backslash and the character it escapes (an escaped quote does not end the string)
            if c == "\\":
                out.append(s[i:i + 2]); i += 2; continue
            out.append(c); i += 1
            if c == quote:
                break
        # the string's span is recorded (a backslash at a line's end continues it on the next line)
        self.literals.append((self.i, i))
        self.i = i; self.prev = "str"

    def _scan_regex(self):
        """Copy a regular-expression literal whole — /…/ with its flags — so a "//" or quote inside it is not misread."""
        s, n, out = self.s, self.n, self.out
        out.append("/")
        i = self.i + 1
        # inside a character class [...] a "/" does not end the expression
        in_class = False
        while i < n:
            c = s[i]
            # an escape: copy it with the character it escapes
            if c == "\\":
                out.append(s[i:i + 2]); i += 2; continue
            # a regular expression cannot span lines: stop at any line terminator (a division misread as one ends here)
            if c in LINE_TERMINATORS:
                break
            # a class opens at "[" and closes at "]": a "/" between them is one of the class's characters
            if c == "[":
                in_class = True; out.append(c); i += 1; continue
            if c == "]":
                in_class = False; out.append(c); i += 1; continue
            # the closing "/", then its flags (g, i, m, s, u, y); the expression's span is recorded
            if c == "/" and not in_class:
                out.append(c); i += 1
                while i < n and s[i].isalpha():
                    out.append(s[i]); i += 1
                self.literals.append((self.i, i))
                self.i = i; self.prev = "regex"; return
            # any other character belongs to the pattern and is copied as it is: a quote in a pattern starts no string
            out.append(c); i += 1
        # the line ended before a closing "/": what was read still counts as one token, and is recorded as one
        self.literals.append((self.i, i))
        self.i = i; self.prev = "regex"

    def _scan_ident(self):
        """Copy a name or keyword; an expression keyword (return, typeof …) lets a following "/" start a regex."""
        s, n = self.s, self.n
        j = self.i
        # a JavaScript identifier: letters, digits, "_" and "$"
        while j < n and (s[j].isalnum() or s[j] == "_" or s[j] == "$"):
            j += 1
        word = s[self.i:j]
        self.out.append(word)
        self.i = j
        # the word is kept, so a "(" after `if`, `while`, `for` or `with` can be told from a call's
        self.last_word = word
        self.prev = "kw_expr" if word in REGEX_PRECEDING_KEYWORDS else "ident"

    def _scan_template(self):
        """Copy a template literal whole; each ${…} inside it is scanned as code again (it may hold comments). The
        template's text is recorded piece by piece — from the opening backtick or an interpolation's closing brace to the
        next "${" or the closing backtick — so the code inside an interpolation is measured as code, not as text."""
        s, n, out = self.s, self.n, self.out
        out.append("`")
        # where the current text piece starts: the opening backtick, then each interpolation's closing brace; the
        # template's pieces learn where it ends once it does
        piece, pieces = self.i, []
        i = self.i + 1
        while i < n:
            c = s[i]
            # an escape: copy it with the character it escapes (an escaped backtick does not end the template)
            if c == "\\":
                out.append(s[i:i + 2]); i += 2; continue
            # the closing backtick ends the template and its last text piece
            if c == "`":
                out.append(c); i += 1; self.i = i; self.prev = "str"
                self._end_template(pieces + [(piece, i)], i)
                return
            # an interpolation: the text piece ends before it, and its expression is code, scanned by _scan_code up to
            # its closing brace, which starts the next text piece
            if c == "$" and i + 1 < n and s[i + 1] == "{":
                pieces.append((piece, i))
                out.append("${"); self.i = i + 2; self.prev = "op"
                self._scan_code(top=False)
                # the field's closing brace, copied, starts the next text piece; the scan goes on after it
                piece = self.i
                if self.i < self.n and self.s[self.i] == "}":
                    out.append("}"); self.i += 1
                i = self.i
                continue
            # any other character of the template's text
            out.append(c); i += 1
        # the text ended inside the template: its last piece runs to the end
        self._end_template(pieces + [(piece, i)], i)
        self.i = i; self.prev = "str"

    def _end_template(self, pieces, end):
        """Record a template's text pieces as literals, each with the offset where the whole template ends."""
        # the pieces in order, each knowing its template's end
        for a, b in pieces:
            self.literals.append((a, b))
            self.literal_ends[a] = end

    def _line_comment(self, i):
        """Remove a comment that runs from i to the line's end (`//`, or an HTML-like `<!--` or `-->`), and record it."""
        s, n, out = self.s, self.n, self.out
        pw = _preceding_ws_count(out)
        j = i
        # the comment ends at the first line terminator, where V8 ends it
        while j < n and s[j] not in LINE_TERMINATORS:
            j += 1
        self.comments.append((i, j))
        # alone on its line: drop its indentation and its line break (CR LF as one), so no blank line is left
        if pw >= 0:
            for _ in range(pw):
                out.pop()
            self.i = (j + (2 if s.startswith("\r\n", j) else 1)) if j < n else j
        # after code: drop the spaces between the code and the comment, keep the line break
        else:
            while out and (out[-1] == " " or out[-1] == "\t"):
                out.pop()
            self.i = j

    def _scan_code(self, top):
        """Scan code up to the end of the text (top) or to the brace that closes a template's ${…} (not top)."""
        s, out = self.s, self.out
        # the braces opened inside this ${…}: its own closing brace is the one met at depth 0
        depth = 0
        while self.i < self.n:
            n = self.n
            i = self.i
            c = s[i]
            nx = s[i + 1] if i + 1 < n else ""

            # a closing brace: the end of the ${…} being scanned, or of a block inside it
            if c == "}":
                if not top and depth == 0:
                    return
                if depth > 0:
                    depth -= 1
                out.append(c); self.i = i + 1; self.prev = "rbrace"; continue
            # an opening brace: one level deeper
            if c == "{":
                depth += 1
                out.append(c); self.i = i + 1; self.prev = "op"; continue
            # whitespace is copied and changes nothing
            if c in " \t\r\n":
                out.append(c); self.i = i + 1; continue

            # a line comment runs to the line's end: `//`, `<!--` anywhere and `-->` where only indentation precedes it
            if (c == "/" and nx == "/") or (c == "<" and s.startswith("<!--", i)) or \
                    (c == "-" and s.startswith("-->", i) and _preceding_ws_count(out) >= 0):
                self._line_comment(i)
                continue
            # a block comment runs to its "*/"; what replaces it depends on whether it is alone on its line
            if c == "/" and nx == "*":
                end = s.find("*/", i + 2)
                if end == -1:
                    end = n - 2
                after = end + 2
                self.comments.append((i, after))
                # alone on its line it goes with its indentation and line break; else one space replaces it
                self.i, fill = _drop_comment_line(out, s, n, after, _preceding_ws_count(out))
                if fill:
                    out.append(fill)
                continue

            # a "/" that is not a comment: a regular expression or a division, by what came before
            if c == "/":
                if self._regex_allowed():
                    self._scan_regex()
                else:
                    out.append(c); self.i = i + 1; self.prev = "op"
                continue
            # strings and template literals are copied whole
            if c == '"' or c == "'":
                self._scan_string(c); continue
            if c == "`":
                self._scan_template(); continue
            # a name or a keyword, read whole: whether it is `return`, `typeof` … decides what a "/" after it means
            if c.isalpha() or c == "_" or c == "$":
                self._scan_ident(); continue
            # a digit: a number, after which "/" divides
            if c.isdigit():
                out.append(c); self.i = i + 1; self.prev = "num"; continue
            # x++ / x-- end an operand like a number does: a "/" after them divides
            if c == "+" and nx == "+":
                out.append("++"); self.i = i + 2; self.prev = "num"; continue
            if c == "-" and nx == "-":
                out.append("--"); self.i = i + 2; self.prev = "num"; continue
            # the point of a decimal number keeps it a number
            if c == "." and self.prev == "num":
                out.append("."); self.i = i + 1; self.prev = "num"; continue
            # an opening parenthesis remembers whether it heads `if`, `while`, `for` or `with`; its closing one then lets
            # a "/" start a regular expression, where after a call's or a group's it divides
            if c == "(":
                self.parens.append(self.prev == "ident" and self.last_word in REGEX_AFTER_PAREN_KEYWORDS)
                out.append(c); self.i = i + 1; self.prev = "op"; continue
            if c == ")":
                heads = self.parens.pop() if self.parens else False
                out.append(c); self.i = i + 1; self.prev = "kw_paren" if heads else "rparen"; continue
            # a closing bracket ends an operand: a "/" after it divides
            if c == "]":
                out.append(c); self.i = i + 1; self.prev = "rbracket"; continue
            # any other character is an operator or punctuation: a "/" after it starts a regular expression
            out.append(c); self.i = i + 1; self.prev = "op"
        return


class HtmlCssStripper:
    """Removes the comments from the markup around the script — <!-- … --> — and from the CSS of each <style> element —
    /* … */ — recording where each comment was, and where each <style> element's CSS lies. A tag is read whole, its
    quoted attribute values included, so a "<!--" or ">" inside a value is text, as it is to the browser."""

    # the stripper's state: the text and where it reads, what it has written, and the spans it found
    def __init__(self, s):
        # one pass over the text, as in JSStripper: the read position `i` only moves forward
        self.s = s
        self.i = 0
        self.n = len(s)
        # the stripped text, built piece by piece
        self.out = []
        # (start, end) of every comment removed, in the coordinates of `s`
        self.comments = []
        # (start, end) of the CSS inside each <style> element, in the coordinates of `s`
        self.css_regions = []

    def _tag_end(self, i):
        """The offset of the ">" that ends the tag starting at i (or the text's length): a quote starts a value only after
        an attribute's "=", and the value it quotes is skipped whole."""
        s, n = self.s, self.n
        j = i + 1
        while j < n and s[j] != ">":
            # an attribute value starts after "=" and any spaces
            if s[j] == "=":
                j += 1
                while j < n and s[j] in " \t\r\n":
                    j += 1
                # a quoted value runs to its closing quote, skipped whole; an unquoted one is read on as the tag's text
                if j < n and s[j] in "\"'":
                    k = s.find(s[j], j + 1)
                    j = n if k == -1 else k + 1
                continue
            # any other character of the tag
            j += 1
        return j

    def run(self):
        """The markup and CSS without their comments (self.comments and self.css_regions hold where things were)."""
        s, n, out = self.s, self.n, self.out
        while self.i < n:
            i = self.i
            # a tag — "<" then a name or "/" — is copied whole to its ">" (a tag left open runs to the text's end)
            if s[i] == "<" and i + 1 < n and (s[i + 1].isalpha() or s[i + 1] == "/"):
                j = self._tag_end(i)
                if j >= n:
                    out.append(s[i:]); self.i = n; break
                out.append(s[i:j + 1]); self.i = j + 1
                # a <style> element's CSS starts after its opening tag and ends where "</style>" begins (css_end)
                if s[i:i + 6].lower() == "<style" and not s[i + 6:i + 7].isalnum():
                    css_start = self.i
                    self._scan_css()
                    self.css_regions.append((css_start, self.css_end))
                continue
            # a markup comment runs to its "-->"
            if s[i:i + 4] == "<!--":
                end = s.find("-->", i + 4)
                if end == -1:
                    self.comments.append((i, n))
                    self.i = n; break
                # recorded, then removed: alone on its line(s) it goes with its indentation and line break; after markup
                # nothing replaces it
                after = end + 3
                self.comments.append((i, after))
                self.i, _ = _drop_comment_line(out, s, n, after, _preceding_ws_count(out))
                continue
            # any other markup character is copied
            out.append(s[i]); self.i = i + 1
        return "".join(out)

    def _scan_css(self):
        """Scan a <style> element's CSS up to its </style>, removing /* … */ comments; strings and url(…) are copied
        whole, so a "/*" inside them stays."""
        s, n, out = self.s, self.n, self.out
        while self.i < n:
            i = self.i
            # the end of the element: the CSS ends where "</style>" begins (css_end), and the tag is copied and passed
            if s[i:i + 8].lower() == "</style>":
                self.css_end = i
                out.append("</style>"); self.i = i + 8
                return
            c = s[i]
            # a quoted string: copied whole, escapes included
            if c == '"' or c == "'":
                out.append(c); i += 1
                while i < n:
                    d = s[i]
                    # an escape: copied with the character it escapes (an escaped quote does not end the string)
                    if d == "\\":
                        out.append(s[i:i + 2]); i += 2; continue
                    out.append(d); i += 1
                    if d == c:
                        break
                self.i = i; continue
            # url(…): copied whole (an unquoted URL may hold "//")
            if s[i:i + 4].lower() == "url(":
                out.append(s[i:i + 4]); i += 4
                while i < n and s[i] != ")":
                    out.append(s[i]); i += 1
                # the closing parenthesis, when the text has one
                if i < n:
                    out.append(")"); i += 1
                self.i = i; continue
            # a CSS comment runs to its "*/"; what replaces it depends on whether it is alone on its line
            if c == "/" and i + 1 < n and s[i + 1] == "*":
                end = s.find("*/", i + 2)
                if end == -1:
                    end = n - 2
                after = end + 2
                self.comments.append((i, after))
                # alone on its line it goes with its indentation and line break; else one space replaces it
                self.i, fill = _drop_comment_line(out, s, n, after, _preceding_ws_count(out))
                if fill:
                    out.append(fill)
                continue
            # any other CSS character is copied
            out.append(c); self.i = i + 1
        # no "</style>" before the text's end: the CSS runs to the end
        self.css_end = n
        return


def strip_comments(text):
    """The app without any comment: the markup and CSS before and after the inline script, and the script itself."""
    a = text.index(OPEN)
    b = text.index(CLOSE)
    assert a < b
    pre = text[:a]
    js = text[a + len(OPEN):b]
    tail = text[b:]
    # each part through its own stripper, the script markers kept
    return HtmlCssStripper(pre).run() + OPEN + JSStripper(js).run() + HtmlCssStripper(tail).run()
