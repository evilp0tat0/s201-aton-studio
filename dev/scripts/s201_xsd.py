"""The S-201 Ed 2.0.0 Annex B XSD, loaded hermetically: one loader for pre-commit check #20 and the browser gate's XSD
leg (run-browser-smoke-gate.py), so the two validate against the same schema the same way.

The schema (dev/spec-sources/s-201-xsd/S-201_Ed2.0.0_Annex_B_DataProductFormatSchemas.xsd) imports the S-100 GML
schemas from https://schemas.s100dev.net/schemas/S100/5.0.0/S100GML/20220620/ (L12-13), and the bundled xlink.xsd
imports http://www.w3.org/2001/xml.xsd; the resolver maps both to the bundled copies under
dev/spec-sources/s-100-xsd/S100/5.0.0/, the parser has the network off, and a remote URL left unmapped is an error.

What the schema can prove: it declares the member elements as untyped local elements (group MemberObjects,
L8035-8107), so it checks the root and its namespace, the S-100 DatasetType (boundedBy, the identification block with
its fixed values and order), the single members wrapper, and each member's name and namespace; a member's content only
laxly — an element with a global declaration in the imported schemas (S100:pointProperty, S100:Point, gml:pos) is
validated, a feature's properties are not — so feature content stays the in-app validator's (FC 2.0.0).

A snapshot tree (dev/scripts/build-public-snapshot.py) ships no reference schema: `snapshot_tree()` tells it from the
development tree, where a missing schema is an error.
"""
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
XSD_REL = os.path.join("dev", "spec-sources", "s-201-xsd", "S-201_Ed2.0.0_Annex_B_DataProductFormatSchemas.xsd")
_S100_REL = os.path.join("dev", "spec-sources", "s-100-xsd", "S100", "5.0.0")


def snapshot_tree(root=ROOT):
    """A tree cut by build-public-snapshot.py: it carries dev/SNAPSHOT.json and not the development docs
    (dev/HANDOFF.md). The marker alone never downgrades the development tree."""
    return (os.path.isfile(os.path.join(root, "dev", "SNAPSHOT.json"))
            and not os.path.isfile(os.path.join(root, "dev", "HANDOFF.md")))


def xsd_path(root=ROOT):
    return os.path.join(root, XSD_REL)


def load(root=ROOT):
    """(schema, xsd_doc) for the S-201 2.0.0 Annex B XSD under `root`.

    Raises FileNotFoundError when the schema is not in the tree, ImportError when lxml is not installed, and
    RuntimeError when the schema reaches a remote URL the resolver does not map to a bundled copy."""
    path = xsd_path(root)
    if not os.path.exists(path):
        raise FileNotFoundError(XSD_REL.replace(os.sep, "/"))
    from lxml import etree
    s100 = os.path.join(root, _S100_REL)
    remote = [
        ("https://schemas.s100dev.net/schemas/S100/5.0.0/S100GML/20220620/", os.path.join(s100, "S100GML", "20220620")),
        ("http://www.w3.org/2001/xml.xsd", os.path.join(s100, "w3c", "XML", "2001", "xml.xsd")),
    ]
    unmapped = []

    class _Bundled(etree.Resolver):
        def resolve(self, url, pubid, context):
            if not (url.startswith("http://") or url.startswith("https://")):
                return None
            for prefix, local in remote:
                if url == prefix:
                    return self.resolve_filename(local, context)
                if prefix.endswith("/") and url.startswith(prefix):
                    return self.resolve_filename(os.path.join(local, url[len(prefix):]), context)
            unmapped.append(url)
            return None

    parser = etree.XMLParser(no_network=True, resolve_entities=False)
    parser.resolvers.add(_Bundled())
    xsd_doc = etree.parse(path, parser)
    schema = etree.XMLSchema(xsd_doc)
    if unmapped:
        raise RuntimeError("the S-201 2.0.0 XSD reached remote URLs that are not mapped to a bundled copy: %s" % unmapped)
    return schema, xsd_doc


def parse(text):
    """The document `text` holds, parsed with the network and entity expansion off; raises lxml's XMLSyntaxError
    when it is not well-formed."""
    from lxml import etree
    return etree.fromstring(text.encode("utf-8"), etree.XMLParser(no_network=True, resolve_entities=False))


def problems(schema, text, limit=3):
    """[] when `text` is well-formed and valid against `schema`; else up to `limit` lines saying why ("not
    well-formed — …", or "L<line> <message>" per schema error)."""
    from lxml import etree
    try:
        doc = parse(text)
    except etree.XMLSyntaxError as e:
        return ["not well-formed — %s" % e]
    if schema.validate(doc):
        return []
    return ["L%s %s" % (err.line, err.message) for err in list(schema.error_log)[:limit]]
