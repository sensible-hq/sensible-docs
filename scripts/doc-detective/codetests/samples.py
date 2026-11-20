"""Sample doc types: the page's own samples, each run in a doc type named for its page and test. They
stay in the test account until the test's next run, so a report's editor links open what ran."""

import os
import re

from . import markup, settings

# Sample doc types keep their names from run to run, so an older report's editor links show newer configs
LINKS_NOTE = ("Each run deletes and recreates these doc types with the page's current samples, so the editor links show the latest run's configs. For exactly what this run ran, see its extraction.")


def page_slug(path):
    """A doc type name part for a page: its file name, lowercase, with other characters as underscores."""
    return re.sub(r"[^a-z0-9]+", "_", os.path.splitext(os.path.basename(path))[0].lower()).strip("_")


def prefix(path):
    """The name prefix of a page's sample doc types, so cleanup only touches this page's."""
    return f"{settings.SAMPLE_DOC_TYPE_PREFIX}{page_slug(path)}__"


def doc_types(test):
    """The sample doc type names a test runs in, in order (see each claim kind's sample_doc_types)."""
    from . import kinds

    return kinds.of(test).sample_doc_types(test)


def create(client, name, config, config_text, document_url, schema=None):
    """Recreate a sample doc type, publish its first config, and add the example document as a reference
    document linked to that config (Sensible needs the config to exist first). Returns (doc type ID,
    reference name or None, when the example document isn't in this repo)."""
    type_id = client.create_sample_doc_type(name, schema)
    client.publish_config(type_id, config, config_text)
    pdf = markup.local_pdf(document_url)
    reference = os.path.splitext(os.path.basename(pdf))[0] if pdf else None
    if pdf:
        client.add_reference(type_id, reference, config, pdf)
    return type_id, reference
