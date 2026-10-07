// GET  /tallies            -> { "102": [up, down], ... }
// POST /vote {id, value}   -> { up, down }   value is 1, -1, or 0 to withdraw
// One vote per result per client address; the address is stored only as a salted hash.

const MAX_ID = 377;

function cors(env) {
  return {
    "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

function json(env, body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...cors(env), ...extra },
  });
}

async function voterHash(request, env) {
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const bytes = new TextEncoder().encode(env.VOTE_SALT + "|" + ip);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function tally(env, id) {
  const row = await env.DB.prepare(
    "SELECT COALESCE(SUM(value = 1), 0) AS up, COALESCE(SUM(value = -1), 0) AS down FROM votes WHERE result_id = ?"
  ).bind(id).first();
  return { up: row.up, down: row.down };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    try {
      if (request.method === "OPTIONS") {
        return new Response(null, { status: 204, headers: cors(env) });
      }
      if (request.method === "GET" && url.pathname === "/tallies") {
        const { results } = await env.DB.prepare(
          "SELECT result_id, SUM(value = 1) AS up, SUM(value = -1) AS down FROM votes GROUP BY result_id"
        ).all();
        const out = {};
        for (const r of results) out[r.result_id] = [r.up, r.down];
        return json(env, out, 200, { "Cache-Control": "public, max-age=30" });
      }
      if (request.method === "POST" && url.pathname === "/vote") {
        if (request.headers.get("Origin") !== env.ALLOWED_ORIGIN) return json(env, { error: "origin" }, 403);
        if (Number(request.headers.get("Content-Length") || 0) > 200) return json(env, { error: "too large" }, 413);
        let body;
        try { body = JSON.parse(await request.text()); } catch { return json(env, { error: "bad json" }, 400); }
        const id = String(body.id ?? "");
        const value = body.value;
        if (!/^\d{3}$/.test(id) || Number(id) < 1 || Number(id) > MAX_ID) return json(env, { error: "bad id" }, 400);
        if (![1, -1, 0].includes(value)) return json(env, { error: "bad value" }, 400);
        const voter = await voterHash(request, env);
        if (value === 0) {
          await env.DB.prepare("DELETE FROM votes WHERE result_id = ? AND voter = ?").bind(id, voter).run();
        } else {
          await env.DB.prepare(
            "INSERT INTO votes (result_id, voter, value, updated_at) VALUES (?, ?, ?, ?) " +
            "ON CONFLICT (result_id, voter) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at"
          ).bind(id, voter, value, Date.now()).run();
        }
        return json(env, await tally(env, id));
      }
      return json(env, { error: "not found" }, 404);
    } catch (err) {
      console.error(JSON.stringify({ message: "unhandled", path: url.pathname, error: String(err) }));
      return json(env, { error: "server" }, 500);
    }
  },
};
