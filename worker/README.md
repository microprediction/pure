# pure-votes

Vote service for the Votes column on `docs/results.html`. A Cloudflare Worker with a D1 table.

```
cd worker
npx wrangler d1 create pure-votes            # paste the database_id into wrangler.jsonc
npx wrangler d1 execute pure-votes --remote --file schema.sql
npx wrangler secret put VOTE_SALT            # any long random string
npx wrangler deploy
```

Then set `VOTE_API` in `scripts/build_results.py` to the Worker URL and rebuild. While `VOTE_API`
is empty the page shows no Votes column.

Each client address gets one vote per result, stored as a salted hash. There is no login.
