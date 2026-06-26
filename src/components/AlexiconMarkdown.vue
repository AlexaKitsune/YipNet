<template>
    <div class="AlexiconMarkdown-MAIN" v-html="result"></div>
</template>

<script>
import { Marked } from 'marked'
import markedKatex from 'marked-katex-extension'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'

import 'highlight.js/styles/tokyo-night-dark.css'
import 'katex/dist/katex.min.css'

const marked = new Marked(
    markedHighlight({
        emptyLangClass: 'hljs',
        langPrefix: 'hljs language-',
        highlight(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext'
            return hljs.highlight(code, { language }).value
        }
    })
)

marked.use(markedKatex({
    throwOnError: false
}))

export default {
    name: 'AlexiconMarkdown',

    props: {
        val: {
            type: String,
            default: ''
        }
    },

    computed: {
        result() {
            const withMentions = this.linkMentions(this.val || '')
            const html = marked.parse(withMentions)
            const processed = this.postProcessing(html)

            return DOMPurify.sanitize(processed, {
                ADD_TAGS: ['iframe'],
                ADD_ATTR: ['allow', 'allowfullscreen', 'frameborder', 'scrolling', 'src', 'width', 'height']
            })
        },
    },

    methods: {
        linkMentions(text) {
            return String(text || '').replace(
                /(^|[^a-zA-Z0-9_])@([a-zA-Z0-9_]{3,32})/g,
                '$1[@$2](/at/$2)'
            );
        },
        
        postProcessing(text) {
            let result = text.replaceAll(
                /<blockquote>\s*<p>!(.*?)<\/p>\s*<\/blockquote>/gs,
                '<div class="AlexiconMarkdown-spoiler"><label><input type="checkbox"/><div>$1</div></label></div>'
            );

            result = result.replaceAll(
                /<p>\s*<a href="https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})[^"]*">[^<]*<\/a>\s*<\/p>/g,
                '<iframe width="100%" height="360" src="https://www.youtube.com/embed/$1" frameborder="0" allowfullscreen></iframe>'
            );

            return result
        }
    }
}
</script>

<style scoped lang="stylus">
.AlexiconMarkdown-MAIN
    font-size: 1.5ch

    :deep(h1)
        font-size: 2em
        font-weight: bold
        margin: 0.5em 0

    :deep(h2)
        font-size: 1.5em
        font-weight: bold
        margin: 0.5em 0

    :deep(strong)
        font-weight: bold

    :deep(em)
        font-style: italic

    :deep(th)
        border: 1px solid rgba(128, 128, 128, 0.2)

    :deep(td)
    :deep(th)
        padding: 0 1ch

    :deep(tbody) > tr:nth-child(odd)
        background-color: rgba(128, 128, 128, 0.2)

    :deep(blockquote)
        border-left: 6px solid rgba(128, 128, 128, 0.2)
        padding-left: 1ch

    :deep(pre) > code
        padding: 1ch
        background-color: rgb(26, 27, 38)
        color: rgb(154, 165, 206)
        font-family: "Roboto Mono", serif
        border-radius: 5px

/* post processing */

    :deep(.AlexiconMarkdown-spoiler)

        label
            position relative;

        div
            padding: 5px 10px;
            background-size: 3px 3px /* Adjusts the spacing of the dots */
            width: fit-content

        input
            position absolute
            opacity 0

            &:not(:checked) ~ div
                cursor: help
                color: transparent
                background-image: radial-gradient(rgba(128, 128, 128, 0.5) 1px, transparent 1px) /* Creates the dots */

            &:checked ~ div
                background-image: radial-gradient(rgba(128, 128, 128, 0.25) 1px, transparent 1px);/* Creates the dots */  

    :deep(iframe)
        border-radius: 5px

    :deep(a)
        color #7700ff
        text-decoration none

        &:hover
            text-decoration underline
</style>
