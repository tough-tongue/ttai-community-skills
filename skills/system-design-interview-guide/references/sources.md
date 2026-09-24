# Source Files: extraction and chapter map

This skill works from source material the user supplies: book chapters they
own, PDFs, exported notes, or pasted text. Do not reconstruct a book chapter
from memory; ask for the source if none is provided.

## Extracting text

Run `file -b` on every new source; `scripts/extract_source.sh <file> out.txt`
branches on the result:

| Actual format | What the script does |
|---|---|
| ZIP archive of page text (`1.txt, 2.txt …`, sometimes with `.jpeg` page images and a `manifest.json`), even when named `.pdf` | Concatenates pages in numeric order and strips CRs. Pages flagged `has_visual_content: true` in the manifest contain diagrams — view the matching `.jpeg` if you need the book's picture. |
| Real PDF | `pdftotext -layout` |
| Plain text (including text dumps with a `.pdf` extension) | Copies it with CRs stripped |

For a whole-book text dump of Alex Xu's *System Design Interview*,
`scripts/extract_xu_chapter.py <file> "<title fragment>"` prints one chapter
(`--list` prints chapter titles). Each title occurs twice in such dumps
(TOC + body); the script takes the body.

## Chapter map

**Alex Xu, *System Design Interview* (Vol. 1)** — ch 1 scale from zero; 2 estimation; 3 interview framework; 4 rate limiter; 5 consistent hashing; 6 key-value store; 7 unique ID generator (Snowflake); 8 URL shortener; 9 web crawler; 10 notification system; 11 news feed; 12 chat system; 13 search autocomplete; 14 YouTube; 15 Google Drive.

**Grokking the System Design Interview** — common chapters: Pastebin, URL Shortening, Instagram, Dropbox, Facebook Messenger, Twitter, YouTube/Netflix, Typeahead Suggestion, API Rate Limiter, Twitter Search, Web Crawler, Facebook Newsfeed, Yelp/Nearby Friends, Uber Backend, Ticketmaster. If a supplied chapter file has no meaningful name, extract it and check its first page.

**Topic → sources**

| Topic | Grokking | Xu | Notes |
|---|---|---|---|
| Rate limiter | ✓ | Ch 4 | Xu richer on algorithms |
| URL shortener / Pastebin | ✓ | Ch 8 | |
| Typeahead / autocomplete | ✓ | Ch 13 | Xu = ground truth for numbers |
| Twitter Search | ✓ | — (Ch 5, 7 as building blocks) | Sibling of Yelp |
| Twitter / Newsfeed | ✓ | Ch 11 | Fan-out theory canonical home = Newsfeed |
| Messenger / chat | ✓ | Ch 12 | |
| YouTube / Netflix | ✓ | Ch 14 | |
| Dropbox / Google Drive | ✓ | Ch 15 | |
| Web crawler | ✓ | Ch 9 | |
| Yelp / Nearby Friends, Uber | ✓ | — | Spatial indexing canonical home = Yelp |
| Instagram, Ticketmaster | ✓ | — | |
| Notification system, KV store, unique ID | — | Ch 10, 6, 7 | |

## Cross-reference discipline

Guides form a family. Shared theory has one canonical home and other guides cite it rather than re-derive: fan-out & celebrity hot keys → Newsfeed; TweetID/Snowflake sharding analysis → Twitter; spatial indexing (geohash/quadtree) → Yelp; scatter-gather top-k → first appears in Yelp, reused by Uber and Twitter Search. Ask the user which sibling guides already exist if unsure.
