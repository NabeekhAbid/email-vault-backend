revision = "0000000002"
down_revision = "0000000001"



def upgrade(migration):
    # write migration here

    migration.update_version_table(version=revision)


def downgrade(migration):
    # write migration here

    migration.update_version_table(version=down_revision)

