<template>
  <main>
    <div v-html="processedText"></div>
  </main>
</template>

<script>
import katex from 'katex';
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';
export default {
  name: "MarkdownRenderer",
  props: {
    postId: String,
    text: String,
  },
  data() {
    return {
      processedText: "",
      footNotes: false
    };
  },
  watch: {
    text: "processText",
  },
  
  mounted() {
    this.processText();
  },

  methods: {
    formatoNegritaCursiva(match, p1, p2, p3, p4, p5, p6) {
      if (match.startsWith("***") && match.endsWith("***")) return `<!--md--><b><i>${p1}</i></b><!--end.md-->`;
      if (match.startsWith("**") && match.endsWith("**")) return `<!--*md--><b>${p2}</b><!--*end.md-->`;
      if (match.startsWith("*") && match.endsWith("*")) return `<!--*md--><i>${p3}</i><!--*end.md-->`;
      if (match.startsWith("__") && match.endsWith("__")) return `<!--_md--><b>${p4}</b><!--_end.md-->`;
      if (match.startsWith("_") && match.endsWith("_")) return `<!--_md--><i>${p5}</i><!--_end.md-->`;
      if (match.startsWith("~~") && match.endsWith("~~")) return `<!--md--><del>${p6}</del><!--end.md-->`;
      if (match.startsWith("`") && match.endsWith("`")) return `<!--md--><span style="font-family:monospace; background-color:rgba(111,111,111,0.5); padding:0 0.5ch; border-radius:0.5ch;">${match.replaceAll("`", "")}</span><!--'end.md-->`;
      return match;
    },

    reemplazarFootnotes(texto) {
      // Usar replace con una expresión regular y grupos de captura
      const resultado = texto.replace(/\[\^(\d+)\]/g, `<a onclick="try{document.getElementById('footnote-$1').scrollIntoView({ behavior: 'smooth'})} catch(e){console.log(e)}" id="footnote-$1"><sup>$1</sup></a>`);
      return resultado;
    },

    renderKatex(formula_){
      return katex.renderToString(formula_, {
          throwOnError: false,
      });
    },

    reemplazarExpresiones(match, expresion) {
      const resultadoRenderizado = this.renderKatex(expresion.replaceAll("<br>",""));
      return resultadoRenderizado.replace('class="katex-html"', 'class="katex-html" style="display:none;"');
    },

    renderCode(code_, lang_){
      let highlightedCode;
      try {
        highlightedCode = hljs.highlight(lang_, code_.replaceAll("$LT;","<").replaceAll("$GT;",">")).value;
      } catch (error) {
        highlightedCode = hljs.highlight("txt", code_.replaceAll("$LT;","<").replaceAll("$GT;",">")).value;
      }
      
      return `<pre style="background-color:rgba(0,0,0,0.1); padding:1ch; border-radius:1ch; overflow:auto;"><code>${highlightedCode}</code></pre>`;
    },

    replaceCodeBlocks(inputText) {
      const replacedText = inputText.replace(/```([\s\S]*?(<br\/>)[\s\S]*?)```/g, (match, code) => {
        // Reemplaza los <br/> dentro del código capturado
        const postId = this.postId;
        console.log(code)
        const regexFootNote = new RegExp(`<!--md--><a onclick="try{document.getElementById\\('tonote-${postId}-(\\d+)'\\).scrollIntoView\\({ behavior: 'smooth'}\\)} catch(e){console.log(e)}" id="footnote-${postId}-(\\d+)" style="color:skyblue; text-decoration:none;">`, 'g');
        const regexToNote = new RegExp(`<!--md--><a onclick="try{document.getElementById\\('footnote-${postId}-(\\d+)'\\).scrollIntoView\\({ behavior: 'smooth'}\\)} catch(e){console.log(e)}" id="tonote-${postId}-(\\d+)" style="color:skyblue; text-decoration:none;"><sup>`, 'g');
        const codeWithLineBreaks = code.replace(/<br\/>/g, '\n')
          .replaceAll(`<!--md--><span style="padding:0.5ch 1ch; background-color:rgba(33,33,33,0.5); display:flex;">`, `> `).replaceAll(`</span><!--end.md-->`, ``)
          .replaceAll(`<!--md--><h6 style="margin-bottom:0;">`, `###### `).replaceAll(`</h6><!--end.md-->`, ``)
          .replaceAll(`<!--md--><h5 style="margin-bottom:0;">`, `##### `).replaceAll(`</h5><!--end.md-->`, ``)
          .replaceAll(`<!--md--><h4 style="margin-bottom:0;">`, `#### `).replaceAll(`</h4><!--end.md-->`, ``)
          .replaceAll(`<!--md--><h3 style="margin-bottom:0;">`, `### `).replaceAll(`</h3><!--end.md-->`, ``)
          .replaceAll(`<!--md--><h2 style="margin-bottom:0;">`, `## `).replaceAll(`</h2><!--end.md-->`, ``)
          .replaceAll(`<!--md--><h1 style="margin-bottom:0; font-size:2em;">`, `# `).replaceAll(`</h1><!--end.md-->`, ``)
          .replaceAll(regexFootNote, `[`).replaceAll(`</a><!--:end.md-->`, `]:`)
          .replaceAll(regexToNote, `[`).replaceAll(`</sup></a><!--end.md-->`, `]`)
          .replaceAll(`<!--md--><span style="font-family:monospace; background-color:rgba(111,111,111,0.5); padding:0 0.5ch; border-radius:0.5ch;">`, `\``).replaceAll(`</span><!--'end.md-->`, `\``)
          .replaceAll(`<!--md--><b><i>`, `***`).replaceAll(`</i></b><!--end.md-->`, `***`)
          .replaceAll(`<!--*md--><b>`, `**`).replaceAll(`</b><!--*end.md-->`, `**`)
          .replaceAll(`<!--*md--><i>`, `*`).replaceAll(`</i><!--*end.md-->`, `*`)
          .replaceAll(`<!--_md--><b>`, `__`).replaceAll(`</b><!--_end.md-->`, `__`)
          .replaceAll(`<!--_md--><i>`, `_`).replaceAll(`</i><!--_end.md-->`, `_`)
          .replaceAll(`<!--md--><del>`, `~~`).replaceAll(`</del><!--end.md-->`, `~~`)
          .replaceAll(`<hr style="border:1px solid #505050;">`, `---`)
        return '```' + codeWithLineBreaks + '```';
      });

      const replacedCode = replacedText.replace(/```(\w*)\n([\s\S]+?)\n```|```\n([\s\S]+?)\n```/g, (match, language, code) => {
        if (!language)
          language = 'txt';
        const highlightedCode = this.renderCode(code, language);
        return highlightedCode;
      });

      return replacedCode;
    },

    processText() {
      let text;
      try {
        text = this.text.replaceAll("\r\n", "\n");
        text = text.trim().split("\n");
      } catch (error) {
        text = "";
      }
      
      let result = [];

      const openTags = [];
      const closeTags = [];

      for (let line of text) {
        line = line.replaceAll("<","$LT;").replaceAll(">","$GT;");
        // Aplicar formato negrita/cursiva antes de agregar al resultado
        if(!line.includes('```'))
          line = line.replace(/\*\*\*(.*?)\*\*\*|\*\*(.*?)\*\*|\*(.*?)\*|__(.*?)__|_(.*?)_|~~(.*?)~~|`(.*?)`/g, this.formatoNegritaCursiva);

        // Manejar etiquetas de apertura
        while (openTags.length > 0) {
          line = openTags.pop() + line;
        }
        // Manejar etiquetas de cierre
        while (closeTags.length > 0) {
          line = line + closeTags.pop();
        }

        if (/^\s{0,4}>\s/.test(line) || /^\s{0,4}\$GT;\s/.test(line)) {
          result.push(`<!--md--><span style="padding:0.5ch 1ch; background-color:rgba(33,33,33,0.5); display:flex;">${line.replace("> ", "").replace("$GT; ", "")}</span><!--end.md-->`);
        } else if (/^\s{0,4}######\s/.test(line)) {
          result.push(`<!--md--><h6 style="margin-bottom:0;">${line.replace("###### ", "")}</h6><!--end.md-->`);
        } else if (/^\s{0,4}#####\s/.test(line)) {
          result.push(`<!--md--><h5 style="margin-bottom:0;">${line.replace("##### ", "")}</h5><!--end.md-->`);
        } else if (/^\s{0,4}####\s/.test(line)) {
          result.push(`<!--md--><h4 style="margin-bottom:0;">${line.replace("#### ", "")}</h4><!--end.md-->`);
        } else if (/^\s{0,4}###\s/.test(line)) {
          result.push(`<!--md--><h3 style="margin-bottom:0;">${line.replace("### ", "")}</h3><!--end.md-->`);
        } else if (/^\s{0,4}##\s/.test(line)) {
          result.push(`<!--md--><h2 style="margin-bottom:0;">${line.replace("## ", "")}</h2><!--end.md-->`);
        } else if (/^\s{0,4}#\s/.test(line)) {
          result.push(`<!--md--><h1 style="margin-bottom:0; font-size:2em;">${line.replace("# ", "")}</h1><!--end.md-->`);
        } else if (/^\s{0,4}\[\^\d+\]:/.test(line)) {
          result.push(line.replace(
              /\[\^(\d+)\]:/g,
              `<!--md--><a onclick="try{document.getElementById('tonote-${this.postId}-$1').scrollIntoView({ behavior: 'smooth'})} catch(e){console.log(e)}" id="footnote-${this.postId}-$1" style="color:skyblue; text-decoration:none;">$1</a><!--:end.md-->`
            ));
        } else if (/\[\^\d+\]/.test(line)) {
          result.push(line.replace(
              /\[\^(\d+)\]/g,
              `<!--md--><a onclick="try{document.getElementById('footnote-${this.postId}-$1').scrollIntoView({ behavior: 'smooth'})} catch(e){console.log(e)}" id="tonote-${this.postId}-$1" style="color:skyblue; text-decoration:none;"><sup>$1</sup></a><!--end.md-->`
            ));
        } else if(line.trim().match(/^-{3,}$/)) {
          result.push('<hr style="border:1px solid #505050;">');
        } else {
          result.push(line);
        }
      }

      // Asegurarse de que todas las etiquetas estén cerradas
      while (closeTags.length > 0) {
        result.push(closeTags.pop());
      }
      result = result.join("<br/>");

      //Render math:
      result = result.replaceAll(/\$\$([^$]+)\$\$/g, this.reemplazarExpresiones);
      result = this.replaceCodeBlocks(result);
      this.processedText = result.replaceAll("$LT;","&lt;").replaceAll("$GT;","&gt;").replaceAll(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|])/img, '<a href="$1" style="color:skyblue;">$1</a>');
    },
  },
};

// npm install mathjax@3
</script>

<style scoped>
main:not(pre) {
  color: white;
}

main > div{
  word-break: break-word;
}

.mdlinks,
.mdlinks:visited {
  color: skyblue !important;
}

.hljs {
    white-space: pre;
    overflow-x: auto;
}

</style>
