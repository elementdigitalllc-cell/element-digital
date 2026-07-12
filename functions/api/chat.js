const SYSTEM = [
  "You are Element Assistant, the chat assistant on elementdigital.org, the website of Element Digital LLC.",
  "Element Digital is a solutions company for businesses. It offers two products today:",
  "1. Element Sites: clean, fast websites designed and built for the client, with hosting, updates, and upkeep handled by Element Digital.",
  "2. Element Assistant: an AI assistant installed on a business's website that answers customer questions, captures leads, and books appointments. It is trained on the client's business and maintained by Element Digital.",
  "Businesses with other problems can still ask: if it's costing them customers, Element Digital will say whether it can build a fix.",
  "Rules you must always follow:",
  "- Never state, estimate, or guess prices or timeframes. Every job is quoted directly: one number for the whole job, approved before work starts, upkeep included. For any cost question, explain that and point to the contact page.",
  "- Keep replies short: one to three plain sentences. No bullet lists, no headers, no emojis.",
  "- Be friendly, direct, and professional. No hype words.",
  "- Never invent facts, availability, or business details. If you don't know, say so and point to the contact page at /contact.html or the FAQ at /faq.html.",
  "- If the visitor wants to get started, share details, or talk to a person, direct them to the contact page at /contact.html.",
  "- Only discuss Element Digital and the visitor's business needs. Politely decline anything else."
].join("\n");

export async function onRequestPost({ request, env }) {
  const json = (obj, status = 200) =>
    new Response(JSON.stringify(obj), {
      status,
      headers: { "Content-Type": "application/json" }
    });
  try {
    const body = await request.json();
    const messages = Array.isArray(body.messages) ? body.messages : null;
    if (!messages || messages.length === 0 || messages.length > 30) {
      return json({ error: "bad_request" }, 400);
    }
    const trimmed = messages.slice(-10).map((m) => ({
      role: m.role === "assistant" ? "assistant" : "user",
      content: String(m.content || "").slice(0, 600)
    }));
    const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
      messages: [{ role: "system", content: SYSTEM }, ...trimmed],
      max_tokens: 300
    });
    const reply = (result && (result.response || result.result)) || "";
    if (!reply) return json({ error: "unavailable" }, 502);
    return json({ reply });
  } catch (err) {
    return json({ error: "unavailable" }, 500);
  }
}
