<template>
    <div class="AlexiconCode-MAIN">
        <div class="AlexiconCode-Header">
            <div class="AlexiconCode-Info">
                <UIcon
                    name="i-lucide-file-code"
                    class="size-4"
                />

                <span class="AlexiconCode-Filename">
                    {{ filename || 'Code preview' }}
                </span>

                <span class="AlexiconCode-Language">
                    {{ languageLabel }}
                </span>
            </div>

            <UButton
                :icon="copied ? 'i-lucide-check' : 'i-lucide-copy'"
                :label="copied ? 'Copied' : 'Copy'"
                size="xs"
                variant="ghost"
                color="neutral"
                @click="copyCode"
            />
        </div>

        <div class="AlexiconCode-Body">
            <div class="AlexiconCode-Lines">
                <span
                    v-for="line in lineCount"
                    :key="line"
                >
                    {{ line }}
                </span>
            </div>

            <pre class="AlexiconCode-Pre"><code v-html="renderedCode" /></pre>
        </div>
    </div>
</template>

<script>
import hljs from 'highlight.js'
import 'highlight.js/styles/tokyo-night-dark.css'

const EXTENSION_LANGUAGE_MAP = {
    js: 'javascript',
    jsx: 'javascript',
    ts: 'typescript',
    tsx: 'typescript',
    vue: 'xml',
    html: 'xml',
    htm: 'xml',
    xml: 'xml',
    svg: 'xml',
    css: 'css',
    json: 'json',
    py: 'python',
    cpp: 'cpp',
    c: 'c',
    h: 'c',
    hpp: 'cpp',
    java: 'java',
    cs: 'csharp',
    go: 'go',
    rs: 'rust',
    php: 'php',
    rb: 'ruby',
    swift: 'swift',
    kt: 'kotlin',
    kts: 'kotlin',
    sh: 'bash',
    zsh: 'bash',
    fish: 'bash',
    ps1: 'powershell',
    bat: 'dos',
    sql: 'sql',
    yaml: 'yaml',
    yml: 'yaml',
    md: 'markdown',
    markdown: 'markdown',
    ini: 'ini',
    toml: 'ini',
    env: 'ini',
    csv: 'plaintext',
    txt: 'plaintext',
    log: 'plaintext'
}

export default {
    name: 'AlexiconCode',

    props: {
        val: {
            type: String,
            default: ''
        },

        filename: {
            type: String,
            default: ''
        },

        extension: {
            type: String,
            default: ''
        }
    },

    data() {
        return {
            copied: false,
            copiedTimeout: null
        }
    },

    computed: {
        code() {
            return this.val || ''
        },

        lineCount() {
            return Math.max(this.code.split('\n').length, 1)
        },

        language() {
            return EXTENSION_LANGUAGE_MAP[this.extension] || 'plaintext'
        },

        languageLabel() {
            if (this.language === 'plaintext') return 'Text'
            if (this.language === 'xml' && this.extension === 'vue') return 'Vue'
            if (this.language === 'xml' && this.extension === 'svg') return 'SVG'
            if (this.language === 'xml') return 'HTML/XML'

            return this.language
        },

        renderedCode() {
            if (!this.code) return ''

            try {
                if (hljs.getLanguage(this.language)) {
                    return hljs.highlight(this.code, {
                        language: this.language,
                        ignoreIllegals: true
                    }).value
                }

                return hljs.highlightAuto(this.code).value
            } catch {
                return this.escapeHtml(this.code)
            }
        }
    },

    methods: {
        escapeHtml(value) {
            return value
                .replaceAll('&', '&amp;')
                .replaceAll('<', '&lt;')
                .replaceAll('>', '&gt;')
        },

        async copyCode() {
            await navigator.clipboard.writeText(this.code)

            this.copied = true

            clearTimeout(this.copiedTimeout)

            this.copiedTimeout = setTimeout(() => {
                this.copied = false
            }, 1500)
        }
    },

    beforeUnmount() {
        clearTimeout(this.copiedTimeout)
    }
}
</script>

<style scoped lang="stylus">
.AlexiconCode-MAIN
    overflow hidden
    border-radius 8px
    background rgb(26, 27, 38)
    color rgb(154, 165, 206)
    border 1px solid rgba(255, 255, 255, 0.08)

.AlexiconCode-Header
    display flex
    align-items center
    justify-content space-between
    gap 1rem
    padding 0.55rem 0.75rem
    background rgba(255, 255, 255, 0.04)
    border-bottom 1px solid rgba(255, 255, 255, 0.06)

.AlexiconCode-Info
    display flex
    align-items center
    gap 0.5rem
    min-width 0

.AlexiconCode-Filename
    max-width 260px
    overflow hidden
    text-overflow ellipsis
    white-space nowrap
    font-size 0.78rem
    opacity 0.9

.AlexiconCode-Language
    flex none
    border-radius 999px
    padding 0.12rem 0.45rem
    background rgba(255, 255, 255, 0.08)
    font-size 0.68rem
    text-transform uppercase
    letter-spacing 0.04em
    opacity 0.75

.AlexiconCode-Body
    display grid
    grid-template-columns auto 1fr
    max-height 420px
    overflow auto

.AlexiconCode-Lines
    user-select none
    padding 1rem 0.65rem
    background rgba(0, 0, 0, 0.18)
    border-right 1px solid rgba(255, 255, 255, 0.05)
    color rgba(154, 165, 206, 0.45)
    text-align right
    font-family ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace
    font-size 0.78rem
    line-height 1.55

.AlexiconCode-Lines span
    display block

.AlexiconCode-Pre
    margin 0
    padding 1rem
    min-width 0
    overflow visible
    font-family ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace
    font-size 0.78rem
    line-height 1.55

.AlexiconCode-Pre code
    display block
    white-space pre
</style>