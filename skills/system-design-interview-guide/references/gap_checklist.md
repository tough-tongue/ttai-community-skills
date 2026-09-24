# Gap Checklist — what the books usually omit

Use this after extraction to decide what to supplement (☆) and what to web-search. Web-search when the gap needs a specific real-world figure or a named company's approach; use general knowledge for textbook material.

## Every topic
- **API definition** — Xu often has one, Grokking sometimes; when missing, write a minimal REST/function signature with a parameter table.
- **Data model** — almost always missing; write `Data | Shape | Where it lives` plus a tiny worked example.
- **Real-world use** (Part 1.2) — who runs this and why it matters commercially. Good web-search targets: the company engineering blog post the chapter alludes to (Facebook "Life of a Typeahead Query", Twitter Snowflake, Uber H3, Dropbox Magic Pocket, Netflix Open Connect).
- **Life-of-a-request walkthrough** — never in the books; always add.
- **Freshness / propagation delay** — books say "periodically"; propose a bound and a mechanism.
- **Deletion / edits / takedowns** — usually absent; the two-stage answer (filter at read, purge async) applies almost everywhere.
- **Observability and what "highly available" means concretely** — one paragraph is enough.

## By family
- **Search / index (Typeahead, Twitter Search, Web Crawler):** ranking staleness; tokenisation beyond English; phrase queries; hot/cold tiering; delta indexes / Lucene segments.
- **Feed / social (Newsfeed, Twitter, Instagram):** hybrid fan-out thresholds; ranking model inputs; unread counts; feed caching TTLs.
- **Spatial (Yelp, Uber):** geohash precision table vs. quadtree; boundary problem; driver location update rate maths; H3/S2 as modern alternatives (web-search for current practice).
- **Storage / files (Dropbox, Drive, Pastebin, URL shortener):** chunking & dedup; sync conflict resolution; block-level vs. file-level; key collision maths.
- **Media (YouTube/Netflix):** transcoding DAG; adaptive bitrate; CDN cost maths; pre-signed upload URLs.
- **Messaging (Messenger, Notification):** delivery guarantees; ordering per conversation; presence heartbeats; push provider fan-out.
- **Control plane (Rate limiter, ID generator, KV store):** algorithm comparison tables; race conditions and their fixes; clock drift.
- **Ticketing / booking (Ticketmaster):** seat locking, overselling, waiting-room queue.

## Discrepancies to surface explicitly
When the two books, or a book and reality, disagree — put it in a blockquote in the estimation or deep-dive section, not a footnote. Known ones: Grokking 5-byte TweetID vs. 8-byte Snowflake; Xu 5 vs. Grokking 10 autocomplete suggestions; Xu weekly vs. Grokking hourly aggregation; Grokking's reconstructed vs. verbatim content in some chapters (note "partially reconstructed" in References).
