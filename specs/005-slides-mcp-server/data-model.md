# Data Model: Slides MCP Server

## Presentation Request

This is the primary data structure that the Slides MCP Server will receive from the slides agent to create a new Google Slides presentation.

```json
{
  "title": "string",
  "template_id": "string", // ID or name of the template presentation/layout to use
  "slides": [
    {
      "layout_id": "string", // Optional: ID or name of a specific layout within the template
      "elements": [
        {
          "type": "string", // e.g., "text", "image", "shape"
          "content": "string", // Required for "text" type
          "image_url": "string", // Required for "image" type
          "position": {
            "x": "number",
            "y": "number",
            "width": "number",
            "height": "number"
          }, // Optional: for precise placement
          "style": {
            "font_size": "number",
            "font_family": "string",
            "color": "string"
          } // Optional: basic styling
        }
      ]
    }
  ]
}
```

### Fields:

-   **`title`** (string, required):
    -   The title of the new Google Slides presentation.
    -   Used for the presentation's name in Google Drive.

-   **`template_id`** (string, required):
    -   An identifier for the pre-saved style/layout template to be used for the presentation.
    -   This will correspond to a specific template presentation or a set of layouts within the dedicated Google Drive folder.

-   **`slides`** (array of objects, required):
    -   A list of slide definitions, each representing a single slide in the presentation.

    #### Slide Object Fields:

    -   **`layout_id`** (string, optional):
        -   An identifier for a specific layout within the chosen `template_id` to apply to this slide.
        -   If not provided, a default layout from the template might be used.

    -   **`elements`** (array of objects, required):
        -   A list of content elements to be placed on the slide.

        #### Element Object Fields:

        -   **`type`** (string, required):
            -   The type of content element. Expected values: `"text"`, `"image"`, `"shape"`.

        -   **`content`** (string, conditional):
            -   The textual content for `"text"` type elements.
            -   Not applicable for `"image"` or `"shape"` types.

        -   **`image_url`** (string, conditional):
            -   The URL of the image for `"image"` type elements.
            -   Not applicable for `"text"` or `"shape"` types.

        -   **`position`** (object, optional):
            -   Defines the placement and size of the element on the slide.
            -   Fields: `x`, `y`, `width`, `height` (numbers, representing relative or absolute units).

        -   **`style`** (object, optional):
            -   Basic styling properties for the element (e.g., `font_size`, `font_family`, `color`).

## Google Slides Presentation

-   The output of the MCP server, a standard Google Slides presentation created via the Google Slides API.
-   Persisted in a shared Google Drive folder owned by a service account.
-   Named using the `title` from the `Presentation Request` suffixed with the current date (e.g., "My Presentation 2025-09-30").