<template>
    <UCard
        class="mt-3 bg-black/20 border-0"
        :ui="{ root: 'border-0', body: 'p-3' }"
        variant="ghost"
    >
        <!-- Header -->
        <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
                <UIcon
                    :name="icon"
                    class="size-5 shrink-0"
                />

                <div class="min-w-0">
                    <p class="truncate text-sm">
                        {{ filename }}
                    </p>

                    <p class="text-xs opacity-60">
                        {{ file.type || extension || 'Unknown type' }}
                    </p>
                </div>
            </div>

            <div class="flex items-center gap-1">
                <UButton
                    v-if="canPreview"
                    icon="i-lucide-eye"
                    variant="ghost"
                    color="neutral"
                    @click="togglePreview"
                />

                <UButton
                    icon="i-lucide-download"
                    variant="ghost"
                    color="neutral"
                    :to="file.fullUrl"
                    target="_blank"
                />
            </div>
        </div>

        <!-- Preview -->
        <div
            v-if="preview"
            class="mt-3"
        >
            <!-- PDF -->
            <iframe
                v-if="isPdf"
                :src="file.fullUrl"
                class="doc-frame"
            />

            <!-- HTML -->
            <iframe
                v-else-if="isHtml"
                :src="file.fullUrl"
                class="doc-frame"
                sandbox="allow-scripts allow-same-origin"
            />

            <!-- DOCX -->
            <div
                v-else-if="isDocx"
                class="doc-preview docx-preview"
                v-html="docContent"
            />

            <!-- Excel -->
            <div
                v-else-if="isExcel"
                class="doc-preview xlsx-preview"
                v-html="docContent"
            />

            <!-- SVG -->
            <img
                v-else-if="isSvg"
                :src="file.fullUrl"
                class="svg-preview"
            >

            <!-- Audio -->
            <audio
                v-else-if="isAudio"
                class="audio-preview"
                controls
            >
                <source
                    :src="file.fullUrl"
                    :type="file.type"
                >
            </audio>

            <!-- Video -->
            <video
                v-else-if="isVideo"
                class="media-preview"
                controls
            >
                <source
                    :src="file.fullUrl"
                    :type="file.type"
                >
            </video>

            <!-- Fuente -->
            <div
                v-else-if="isFont"
                class="font-preview"
                :style="{ '--preview-font': `'${fontFamilyName}'` }"
            >
                <p>0123456789.:,;*'"¡!¿?(){}[]/\_-+=^#$%&@°|~`´</p>
                <p>THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.</p>
                <p>The quick brown fox jumps over the lazy dog.</p>
                <p>EL VELOZ MURCIÉLAGO HINDÚ COMÍA FELIZ CARDILLO Y KIWI.</p>
                <p>El veloz murciélago hindú comía feliz cardillo y kiwi.</p>
            </div>

            <!-- Modelo 3D -->
            <AlexiconModelViewer
                v-else-if="isModel3D"
                :src="file.fullUrl"
                :extension="extension"
            />

            <!-- Código -->
            <AlexiconCode
                v-else-if="isCode"
                :val="plainContent"
                :filename="filename"
                :extension="extension"
            />

            <!-- Fallback -->
            <div
                v-else
                class="text-sm opacity-60 py-8 text-center"
            >
                Preview not available.
            </div>
        </div>
    </UCard>
</template>

<script>
import mammoth from 'mammoth'
import * as XLSX from 'xlsx'

import AlexiconCode from '@/components/AlexiconCode.vue'
import AlexiconModelViewer from '@/components/AlexiconModelViewer.vue'

const CODE_EXTENSIONS = [
    'txt', 'xml', 'csv', 'js', 'css', 'json',
    'py', 'cpp', 'bat', 'sql',
    'md', 'markdown',
    'ts', 'tsx', 'jsx', 'vue',
    'java', 'c', 'h', 'hpp', 'cs', 'go', 'rs',
    'php', 'rb', 'swift', 'kt', 'kts',
    'sh', 'zsh', 'fish', 'ps1',
    'yaml', 'yml', 'toml', 'ini', 'env',
    'log'
]

export default {
    name: 'AlexiconDoc',

    components: {
        AlexiconCode,
        AlexiconModelViewer
    },

    props: {
        file: {
            type: Object,
            required: true
        }
    },

    data() {
        return {
            preview: false,
            plainContent: '',
            docContent: '',
            fontFamilyName: '',
            loading: false,
            errorMessage: ''
        }
    },

    computed: {
        filename() {
            return this.file.filename || this.file.name || 'File'
        },

        extension() {
            const name = this.filename || ''
            return name.includes('.')
                ? name.split('.').pop().toLowerCase()
                : ''
        },

        mimeType() {
            return this.file.type || ''
        },

        isPdf() {
            return this.mimeType === 'application/pdf' || this.extension === 'pdf'
        },

        isHtml() {
            return ['html', 'htm'].includes(this.extension)
        },

        isDocx() {
            return this.extension === 'docx'
        },

        isExcel() {
            return ['xls', 'xlsx'].includes(this.extension)
        },

        isSvg() {
            return this.mimeType === 'image/svg+xml' || this.extension === 'svg'
        },

        isAudio() {
            return [
                'mp3', 'wav', 'm4a', 'aac', 'flac', 'ogg'
            ].includes(this.extension)
        },

        isVideo() {
            return [
                'mp4', 'mov', 'webm'
            ].includes(this.extension)
        },

        isFont() {
            return [
                'ttf', 'otf', 'woff'
            ].includes(this.extension)
        },

        isModel3D() {
            return [
                'glb', 'gltf', 'obj', 'stl'
            ].includes(this.extension)
        },

        isCode() {
            return CODE_EXTENSIONS.includes(this.extension)
        },

        canPreview() {
            return (
                this.isPdf ||
                this.isHtml ||
                this.isDocx ||
                this.isExcel ||
                this.isSvg ||
                this.isAudio ||
                this.isVideo ||
                this.isFont ||
                this.isModel3D ||
                this.isCode
            )
        },

        icon() {
            if (this.isPdf || this.isDocx) return 'i-lucide-file-text'
            if (this.isExcel) return 'i-lucide-table'
            if (this.isSvg) return 'i-lucide-image'
            if (this.isAudio) return 'i-lucide-audio-lines'
            if (this.isVideo) return 'i-lucide-film'
            if (this.isFont) return 'i-lucide-case-sensitive'
            if (this.isHtml || this.isCode) return 'i-lucide-file-code'
            if (this.isModel3D) return 'i-lucide-box'

            return 'i-lucide-file'
        }
    },

    methods: {
        async togglePreview() {
            this.preview = !this.preview

            if (!this.preview) return

            await this.preparePreview()
        },

        async preparePreview() {
            this.loading = true
            this.errorMessage = ''

            try {
                if (this.isCode && !this.plainContent) {
                    await this.readPlain()
                }

                if (this.isDocx && !this.docContent) {
                    await this.renderDocx()
                }

                if (this.isExcel && !this.docContent) {
                    await this.renderExcel()
                }

                if (this.isFont && !this.fontFamilyName) {
                    await this.loadFont()
                }
            } catch (error) {
                console.error(error)
                this.errorMessage = 'Could not load preview.'
            } finally {
                this.loading = false
            }
        },

        async getArrayBuffer() {
            const response = await fetch(this.file.fullUrl)

            if (!response.ok) {
                throw new Error('Could not load file.')
            }

            return response.arrayBuffer()
        },

        async readPlain() {
            const response = await fetch(this.file.fullUrl)

            if (!response.ok) {
                throw new Error('Could not load text file.')
            }

            this.plainContent = await response.text()
        },

        async renderDocx() {
            const arrayBuffer = await this.getArrayBuffer()

            const result = await mammoth.convertToHtml({
                arrayBuffer
            })

            this.docContent = result.value || '<p>No preview content.</p>'
        },

        async renderExcel() {
            const arrayBuffer = await this.getArrayBuffer()
            const workbook = XLSX.read(arrayBuffer)
            const sheetName = workbook.SheetNames[0]

            if (!sheetName) {
                this.docContent = '<p>No sheets found.</p>'
                return
            }

            const sheet = workbook.Sheets[sheetName]

            this.docContent = XLSX.utils.sheet_to_html(sheet)
        },

        async loadFont() {
            const cleanName = this.filename.replace(/\.[^/.]+$/, '')
            const fontName = `alexicon-font-${cleanName}-${Date.now()}`
                .replace(/[^a-z0-9_-]/gi, '-')

            const arrayBuffer = await this.getArrayBuffer()

            const font = new FontFace(fontName, arrayBuffer)
            const loadedFont = await font.load()

            document.fonts.add(loadedFont)

            await document.fonts.ready

            this.fontFamilyName = fontName
        },
    }
}
</script>

<style scoped lang="stylus">
.doc-frame
    width 100%
    height 420px
    border 0
    border-radius 8px
    background white

.doc-preview
    max-height 420px
    overflow auto
    border-radius 8px
    padding 1rem
    background white
    color black

.docx-preview :deep(*)
    max-width 100%

.xlsx-preview
    font-size 0.85rem

.xlsx-preview :deep(table)
    border-collapse collapse
    width 100%

.xlsx-preview :deep(td),
.xlsx-preview :deep(th)
    border 1px solid rgba(0, 0, 0, 0.18)
    padding 0.35rem 0.5rem
    white-space nowrap

.svg-preview
    display block
    width 100%
    max-height 420px
    object-fit contain
    border-radius 8px
    padding 1rem
    background white

.media-preview
    display block
    width 100%
    max-height 420px
    border-radius 8px
    background black

.audio-preview
    display block
    width 100%
    margin-top 0.25rem

.font-preview
    max-height 420px
    overflow auto
    border-radius 8px
    padding 1rem
    background rgba(255, 255, 255, 0.06)
    text-align center
    font-size 1.35rem
    line-height 1.7
    font-family var(--preview-font), sans-serif !important

.font-preview *
    font-family var(--preview-font), sans-serif !important

.font-preview p
    margin 0.5rem 0
    
.preview-message
    display flex
    align-items center
    justify-content center
    min-height 160px
    border-radius 8px
    background rgba(255, 255, 255, 0.04)
    font-size 0.875rem
    opacity 0.65
</style>