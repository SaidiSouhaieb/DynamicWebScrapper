# Web Scraping Toolkit

**Introduction:**
This versatile Python package allows users to effortlessly scrape data from a variety of websites, offering a seamless experience in extracting information regardless of the site's structure or design. This project serves as an invaluable resource for anyone seeking to enhance their understanding of web scraping.

**How to Use:**
The package is equipped with a CLI using Click, making it easy to input the necessary parameters for data extraction.

**Usage Steps:**
1. Provide the link of the target site. It can be a page containing numerous links to extract data from, or a single page for direct data extraction.
2. If the link contains multiple links, specify the class name of the "a" tag holding these links. Leave it empty for single-page extraction.
3. Choose the pagination type:
   - `number`: For sites with numbered pagination.
   - `see_more`: For sites with a "see more" button that expands additional information.
   - `none`: For single pages or infinite scroll pages.
4. Specify the class name of the pagination element based on the chosen pagination type.
5. Choose the items to scrape:
   - Provide a name for the item.
   - Select the extraction type:
     - `tag-name`: Using HTML tag names.
     - `class-name`: Using class names.
     - `id`: Using ID.
     - `name`: Using the name attribute.
     - `link-text`: By extracting the text inside an "a" tag.
   - Based on the extraction type, provide the necessary details (e.g., tag name, class name, ID, etc.).
   - If extracting a value inside an attribute, specify the attribute name (e.g., "src" for image URLs).
   - Choose whether to continue adding items or stop.
   
**Tips for Step 5:**
- Use `tag-name` when there is only one tag of that kind (e.g., h1).
- `class-name` is commonly used; ensure it is unique to avoid extracting unintended items.
- Exercise caution with `id` as IDs can vary across pages for the same element.

This project provides a comprehensive solution for web scraping and serves as an excellent learning tool for navigating the intricacies of data extraction from diverse websites.
