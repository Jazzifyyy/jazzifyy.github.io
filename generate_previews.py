import os
from bs4 import BeautifulSoup

# Configuration
BLOG_FOLDER = "./logs"        # The folder containing your HTML blog posts
OUTPUT_FILE = "logs.html" # Change to whatever your main page filename is
PREVIEW_LENGTH = 500            # Number of characters for the excerpt

def generate_blog_index():
    blog_previews = []

    if not os.path.exists(BLOG_FOLDER):
        print(f"Error: The folder '{BLOG_FOLDER}' does not exist.")
        return

    for filename in sorted(os.listdir(BLOG_FOLDER), reverse = True):
        if filename.endswith(".html"):
            file_path = os.path.join(BLOG_FOLDER, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                
                # 1. Grab Title (checks <h1> first, then <title>)
                title_tag = soup.find("h1") or soup.find("title")
                title = title_tag.get_text().strip() if title_tag else filename.replace(".html", "")
                
                # 2. Grab Excerpt (first paragraph)
                first_p = soup.find("p")
                if first_p:
                    excerpt = first_p.get_text().strip()
                    if len(excerpt) > PREVIEW_LENGTH:
                        excerpt = excerpt[:PREVIEW_LENGTH] + "..."
                else:
                    excerpt = "No preview available."

                # 3. Grab the first image (if it exists)
                first_img = soup.find("img")
                img_src = None
                img_alt = "Blog thumbnail"
                
                if first_img and first_img.get("src"):
                    raw_src = first_img["src"]
                    img_alt = first_img.get("alt", title)
                    
                    # Fix pathing relative to your main directory
                    if not raw_src.startswith(("http://", "https://", "/")):
                        img_src = f"{BLOG_FOLDER}/{raw_src}"
                    else:
                        img_src = raw_src

                relative_link = f"{BLOG_FOLDER}/{filename}"
                
                blog_previews.append({
                    "title": title,
                    "excerpt": excerpt,
                    "link": relative_link,
                    "img_src": img_src,
                    "img_alt": img_alt
                })

    # Build the HTML using your exact layout
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=0.7">
    <title>jazzifyy's logs</title>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap" rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=Noto Serif' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container-zen">
    <a href="index.html" class="back-home"><code>cd ..</code></a>
    
    <header>
        <h1><span style="color:white;">jazzifyy</span>'s logs</h1>
        <p><i>Trying to disengage Nostromo's self-destruct sequence.</i></p>
    </header>

    <img src = "lain.gif" style="width: 35%; height: auto;">
    <p>The sole purpose of doing this is so that the reality doesn't feel like a quick blip. This will perhaps make me more grounded, a way to slow down and aid my poor memory, in this terrifyingly fast flow of time.</p> 
    <hr>
    
    <!-- Generated Blog List -->
    <div class="blog-list">
"""

    # Inject each preview card
    for post in blog_previews:
        html_content += f"""
        <div class="blog-card">"""
        
        if post['img_src']:
            html_content += f"""
            <div class="blog-thumbnail">
                <img src="{post['img_src']}" alt="{post['img_alt']}">
            </div>"""
            
        html_content += f"""
            <div class="blog-content">
                <h2>{post['title']}</h2>
                <p>{post['excerpt']}</p>
                <a class="read-more" href="{post['link']}">Read More &rarr;</a>
            </div>
        </div>
"""

    # Close your custom container tags cleanly
    html_content += """
    </div>
</div>

</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        out_file.write(html_content)
        
    print(f"Success! Generated {OUTPUT_FILE} matching your design structure.")

if __name__ == "__main__":
    generate_blog_index()


