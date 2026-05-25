"""Story 6.5d: Seed global FormBuilderComponent backlog (rating, url, file-upload, paragraph, address).

Revision ID: 087
Revises: 086
"""

from alembic import op


revision = "087"
down_revision = "086"
branch_labels = None
depends_on = None


def _esc(s: str) -> str:
    s = s.replace(":true", ": true").replace(":false", ": false")
    for i in range(10):
        s = s.replace(f":{i}", f": {i}")
    return s.replace("'", "''")


_STD_STRUCTURE = (
    '{"objects":[{"id":"label","type":"label","archetype":"PrimaryLabel","required":true,'
    '"order":1},{"id":"input","type":"input","archetype":"InputControl","required":true,'
    '"order":2},{"id":"validation","type":"validation","archetype":"HelperText",'
    '"required":false,"order":3,"conditional":{"type":"validation"}}],'
    '"defaultLayout":"vertical"}'
)
_LAYOUT_V = '{"rows":3,"columns":1,"cellAssignments":{"0-0":"label","1-0":"input","2-0":"validation"}}'
_LAYOUT_H = '{"rows":2,"columns":3,"cellAssignments":{"0-0":"label","0-1":"input","0-2":"validation"}}'
_PROPS_STD = (
    '{"fields":[{"key":"label","type":"string"},{"key":"placeholder","type":"string"},'
    '{"key":"required","type":"boolean"},{"key":"validation","type":"object"},'
    '{"key":"styleOverrides","type":"object"}]}'
)
_DISPLAY_STRUCTURE = (
    '{"objects":[{"id":"content","type":"custom","required":true,"order":1}],'
    '"defaultLayout":"vertical"}'
)
_DISPLAY_LAYOUT = '{"rows":1,"columns":1,"cellAssignments":{"0-0":"content"}}'


def upgrade() -> None:
    scope_global = "SELECT ComponentScopeID FROM [ref].[ComponentScope] WHERE ScopeCode = 'Global'"

    component_types = [
        ("rating", "Rating", "input", 145),
        ("url", "URL", "input", 146),
        ("file-upload", "File Upload", "input", 147),
        ("paragraph", "Paragraph", "display", 148),
        ("address", "Address", "input", 149),
    ]
    for code, display, category, sort_order in component_types:
        op.execute(
            f"""
            IF NOT EXISTS (
                SELECT 1 FROM [ref].[ComponentType]
                WHERE [ComponentTypeCode] = N'{code}' AND [IsActive] = 1
            )
            INSERT INTO [ref].[ComponentType]
                ([ComponentTypeCode], [DisplayName], [Category], [SortOrder], [IsActive])
            VALUES (N'{code}', N'{display}', N'{category}', {sort_order}, 1);
            """
        )

    seeds = [
        ("rating", "Rating", _STD_STRUCTURE, _LAYOUT_V, _LAYOUT_H,
         '{"fields":[{"key":"label","type":"string"},{"key":"ratingMax","type":"number",'
         '"default":5},{"key":"ratingStyle","type":"string","default":"stars"},'
         '{"key":"required","type":"boolean"},{"key":"styleOverrides","type":"object"}]}', 145),
        ("url", "URL", _STD_STRUCTURE, _LAYOUT_V, _LAYOUT_H, _PROPS_STD, 146),
        ("file-upload", "File Upload", _STD_STRUCTURE, _LAYOUT_V, _LAYOUT_H,
         '{"fields":[{"key":"label","type":"string"},{"key":"accept","type":"string"},'
         '{"key":"maxSizeMb","type":"number"},{"key":"required","type":"boolean"},'
         '{"key":"styleOverrides","type":"object"}]}', 147),
        ("paragraph", "Paragraph", _DISPLAY_STRUCTURE, _DISPLAY_LAYOUT, _DISPLAY_LAYOUT,
         '{"fields":[{"key":"text","type":"string"},{"key":"styleOverrides","type":"object"}]}', 148),
        ("address", "Address", _STD_STRUCTURE, _LAYOUT_V, _LAYOUT_H,
         '{"fields":[{"key":"label","type":"string"},{"key":"placeholder","type":"string"},'
         '{"key":"required","type":"boolean"},{"key":"exportName","type":"string",'
         '"default":"address"},{"key":"styleOverrides","type":"object"}]}', 149),
    ]

    for code, display, struct, layout_v, layout_h, props, sort_order in seeds:
        op.execute(
            f"""
            INSERT INTO [dbo].[FormBuilderComponent] (
                ComponentTypeID, ComponentScopeID, ComponentCode, DisplayName, SortOrder,
                PropertiesSchemaJSON, StructureJSON,
                DefaultGridLayoutVerticalJSON, DefaultGridLayoutHorizontalJSON
            )
            SELECT ct.ComponentTypeID, ({scope_global}), N'{code}', N'{display}', {sort_order},
                N'{_esc(props)}', N'{_esc(struct)}',
                N'{_esc(layout_v)}', N'{_esc(layout_h)}'
            FROM [ref].[ComponentType] ct
            WHERE ct.ComponentTypeCode = N'{code}' AND ct.IsActive = 1
            AND NOT EXISTS (
                SELECT 1 FROM [dbo].[FormBuilderComponent] fbc
                JOIN [ref].[ComponentType] c ON fbc.ComponentTypeID = c.ComponentTypeID
                WHERE c.ComponentTypeCode = N'{code}'
                  AND fbc.ComponentScopeID = ({scope_global})
                  AND fbc.IsDeleted = 0
            );
            """
        )


def downgrade() -> None:
    op.execute(
        """
        DELETE fbc
        FROM [dbo].[FormBuilderComponent] fbc
        INNER JOIN [ref].[ComponentType] ct ON fbc.ComponentTypeID = ct.ComponentTypeID
        INNER JOIN [ref].[ComponentScope] cs ON fbc.ComponentScopeID = cs.ComponentScopeID
        WHERE cs.ScopeCode = 'Global'
          AND ct.ComponentTypeCode IN (
              N'rating', N'url', N'file-upload', N'paragraph', N'address'
          );
        """
    )
    op.execute(
        """
        DELETE FROM [ref].[ComponentType]
        WHERE ComponentTypeCode IN (
            N'rating', N'url', N'file-upload', N'paragraph', N'address'
        );
        """
    )
