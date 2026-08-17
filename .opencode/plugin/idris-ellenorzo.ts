import type { Plugin } from "@opencode-ai/plugin"

// ═══════════════════════════════════════════════════════════════
// IDRIS ELLENŐRZŐ PLUGIN — a kritikus szabályok mechanikus
// kikényszerítése minden .idr fájl szerkesztése után.
//
// A projekt lényege: az Idris kód maga a kutatás (leírás +
// bizonyítás + teszt + futtatás). Ezért a szabályszegést azonnal
// jelezni kell, nem a következő fordításnál.
//
// A plugin a projekt gyökerében lévő ellenorzes.sh szkriptet
// futtatja, amely a következőket ellenőrzi:
//   1. rövidítés-alias definíciók tiltása (MH, MS, DG, ...)
//   2. kisbetűs konstansnév bizonyítástípusban (Idris 0.8.0 csapda)
// ═══════════════════════════════════════════════════════════════

export default (async ({ directory, $ }) => {
  return {
    "tool.execute.after": async (input, output) => {
      try {
        const szerkesztettFajlUtvonal =
          typeof output?.metadata?.filePath === "string"
            ? output.metadata.filePath
            : typeof (output as any)?.filePath === "string"
              ? (output as any).filePath
              : ""

        const idrisFajltErinthet =
          szerkesztettFajlUtvonal.endsWith(".idr") ||
          JSON.stringify(input?.args ?? {}).includes(".idr")

        if (!idrisFajltErinthet) return

        const futtatas = await $`bash ellenorzes.sh`.cwd(directory).noThrow()
        const kimenet = futtatas.stdout?.toString() ?? ""

        const szabalySzegesVan = kimenet.includes("SZABÁLYSZEGÉS")
        if (szabalySzegesVan) {
          const figyelmeztetes =
            "\n\n⚠️ ELLENŐRZÉS: Idris szabályszegés történt!\n" +
            kimenet +
            "\nJavítsd a jelzett sorokat. A szabályok oka: rövidítések " +
            "tiltása (a kód önmagában olvasható legyen), és a kisbetűs " +
            "konstansnév bizonyítástípusban implicit kötést okoz (Idris 0.8.0)."
          if (typeof output.output === "string") {
            output.output += figyelmeztetes
          } else {
            ;(output as any).output = figyelmeztetes
          }
        }
      } catch {
        // Az ellenőrzés hibája sosem akadályozza a szerkesztést.
      }
    },
  }
}) satisfies Plugin
