import { readdir, readFile } from "node:fs/promises"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { Plugin, Skill } from "@opencode/plugin"
import { parse } from "yaml"

const skillsRoot = join(dirname(fileURLToPath(import.meta.url)), "skills")
const frontmatter = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/

async function load(id: string): Promise<Skill.Info | undefined> {
  const path = join(skillsRoot, id, "SKILL.md")
  const source = await readFile(path, "utf8").catch(() => undefined)
  if (source === undefined) return undefined
  const match = frontmatter.exec(source)
  const fields = match ? (parse(match[1]) ?? {}) : {}
  return {
    id: Skill.ID.make(id),
    name: Skill.Name.make(fields.name ?? id),
    description: fields.description,
    autoinvoke: fields["disable-model-invocation"] !== true,
    path: Skill.Info.fields.path.make(path),
    content: match ? source.slice(match[0].length) : source,
  }
}

export default Plugin.define({
  id: "subspace",
  async setup(ctx) {
    const entries = await readdir(skillsRoot, { withFileTypes: true })
    const ids = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name)
    const skills = (await Promise.all(ids.sort().map(load))).filter((skill) => skill !== undefined)
    await ctx.skill.transform((editor) => {
      skills.forEach((skill) => editor.add(skill))
    })
  },
})
