DELETE FROM documents WHERE id = 6 OR title = 'Pricing cards';

INSERT INTO documents (id, title, body, created_at, updated_at) VALUES
  (
    1,
    'Access and sign-in requirements',
    $$Home, Articles, Rentals, and Videos are public pages. The dashboard and content management actions require sign-in as an admin user. Only approved users see the Dashboard link and should be granted access in the Rails console. Reach out to site admin for user approval.$$,
    TIMESTAMP '2026-02-23 12:00:00',
    TIMESTAMP '2026-02-23 00:42:58.218239'
  ),
  (
    2,
    'Landing page featured cards',
    $$The home page pulls the latest three LandingCard records. Each card uses a title, description, and optional image filename. Store image files in app/assets/images and reference the filename in the record.

THESE ARE EDITABLE IN ARTICLES SECTION OF DASHBOARD.$$,
    TIMESTAMP '2026-02-23 12:00:00',
    TIMESTAMP '2026-02-23 00:41:42.338974'
  ),
  (
    3,
    'Rentals calendar behavior',
    $$Rentals are displayed in a month calendar. Each rental paints a block for every day between start_time and end_time. The rentals section of the site assumes three dumpsters will always be available. If fewer than three blocks appear on a date, availability is likely (still confirm by phone). The dumpster emoji comes only from the dropdown selection on the rental form.$$,
    TIMESTAMP '2026-02-23 12:00:00',
    TIMESTAMP '2026-02-23 00:43:58.018192'
  ),
  (
    4,
    'Articles and images',
    $$Articles section is 100% managed by getawd.com at this time. It has title, description, body, and optional image. Image fields store a filename only, based on the file in app/assets/images, stored in the image field of db for the record in question.$$,
    TIMESTAMP '2026-02-23 12:00:00',
    TIMESTAMP '2026-02-23 00:45:17.604398'
  ),
  (
    5,
    'Videos and YouTube embeds',
    $$Videos store a youtube_id and render an embedded player. youtube_id is basically the ~8 characters of shit after youtube.com/ in the url for the video in question, and before the ?. Manage videos from the dashboard. IDK, embedding shouldn't be this big of an ordeal.$$,
    TIMESTAMP '2026-02-23 12:00:00',
    TIMESTAMP '2026-02-23 00:46:49.282838'
  )
ON CONFLICT (id) DO UPDATE
SET title = EXCLUDED.title,
    body = EXCLUDED.body,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;
