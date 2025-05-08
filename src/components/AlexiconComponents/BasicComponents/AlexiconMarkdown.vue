<template>
    <div class="AlexiconMarkdown-MAIN" v-html="result"></div>
</template>

<script>
import { Marked } from 'marked';
import markedKatex from "marked-katex-extension";
import { markedHighlight } from "marked-highlight";
import hljs from 'highlight.js';
import 'highlight.js/styles/tokyo-night-dark.css';

export default {
    name: 'AlexiconMarkdown',
    props:{
        styles: Object,
        val: undefined,
    },
    data(){
        return{
            result: '',
        }
    },
    methods: {
        renderMarkdown(){
            const options = {
                throwOnError: false,
            };

            const marked = new Marked(
                markedHighlight({
                    emptyLangClass: 'hljs',
                    langPrefix: 'hljs language-',
                    // eslint-disable-next-line no-unused-vars
                    highlight(code, lang, info) {
                        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
                        return hljs.highlight(code, { language }).value;
                    },
                })
            );
            marked.use(markedKatex(options));

            const html = marked.parse(this.val);
            this.result = html;
        }
    },
    mounted(){
        this.renderMarkdown();
    }
}
</script>

<style scoped>
.AlexiconMarkdown-MAIN{
    font-size: 1.5ch;
}

.AlexiconMarkdown-MAIN >>> th{
    border: 1px solid rgba(128, 128, 128, 0.2);
}

.AlexiconMarkdown-MAIN >>> td, .AlexiconMarkdown-MAIN >>> th{
    padding: 0 1ch;
}

.AlexiconMarkdown-MAIN >>> tbody > tr:nth-child(odd){
    background-color: rgba(128, 128, 128, 0.2);
}

.AlexiconMarkdown-MAIN >>> blockquote{
    border-left: 6px solid rgba(128, 128, 128, 0.2);
    padding-left: 1ch;
}

.AlexiconMarkdown-MAIN >>> pre > code{
    padding: 1ch;
    background-color: rgb(26, 27, 38);
    color: rgb(154, 165, 206);
    font-family: "Roboto Mono", serif;
}
</style>