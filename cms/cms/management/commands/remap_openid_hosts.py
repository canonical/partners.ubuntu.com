"""Remap OpenID identities from login.launchpad.net to login.ubuntu.com.

The staging database's UserOpenID rows were created against
``https://login.launchpad.net/+id/<token>``. Now that
``OPENID_SSO_SERVER_URL`` points at ``https://login.ubuntu.com/`` (the SSO
host the egress proxy actually allows), logins return the *same* ``+id/<token>``
but with the ``login.ubuntu.com`` host, so django_openid_auth's exact-match
lookup misses and — with ``OPENID_CREATE_USERS`` — creates a duplicate user.

Ubuntu SSO issues the same identity token under both hostnames, so rewriting
just the host on the stored claimed_id/display_id makes existing users match
again. Idempotent: rows already on login.ubuntu.com are skipped. Run with
``--dry-run`` first.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from django_openid_auth.models import UserOpenID

OLD_HOST = "https://login.launchpad.net/"
NEW_HOST = "https://login.ubuntu.com/"


class Command(BaseCommand):
    help = "Rewrite UserOpenID hosts from login.launchpad.net to login.ubuntu.com"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without writing.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        rows = UserOpenID.objects.filter(claimed_id__startswith=OLD_HOST)
        count = 0
        for row in rows:
            new_claimed = row.claimed_id.replace(OLD_HOST, NEW_HOST, 1)
            new_display = (row.display_id or "").replace(OLD_HOST, NEW_HOST, 1)
            self.stdout.write(
                "user_id=%s  %s -> %s" % (row.user_id, row.claimed_id, new_claimed)
            )
            if not dry_run:
                row.claimed_id = new_claimed
                row.display_id = new_display
                row.save(update_fields=["claimed_id", "display_id"])
            count += 1

        verb = "Would remap" if dry_run else "Remapped"
        self.stdout.write(self.style.SUCCESS("%s %d identity row(s)." % (verb, count)))
        if dry_run:
            # Don't leave a half-open transaction implying a write happened.
            transaction.set_rollback(True)
