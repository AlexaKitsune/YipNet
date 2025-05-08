<template>
    <div class="AlexiconDoc-MAIN">

        <div>
            <div>
                <button class="Alexicon-icon-btn">
                    <component :is="docData[typeDoc]?.icon" v-if="docData[typeDoc]?.icon"/>
                    <File v-else/>
                </button>
            </div>
            <div>{{ docName }} <span v-if="preview">(quick preview)</span></div>
            <div>
                <button @click="renderByFormat()" v-if="!preview && previewAvailableFormats.includes(typeDoc)" class="Alexicon-icon-btn"><Eye :size="20"/></button>
                <button class="Alexicon-icon-btn"><Download :size="20"/></button>
            </div>
        </div>

        <div v-if="typeDoc == 'pdf' && preview" class="AlexiconDoc-pdf">
            <object :data="src" width="100%">
                <iframe class="pdf" :src="src" width="100%"></iframe>
            </object>
        </div>

        <div v-if="typeDoc == 'docx' && preview" class="AlexiconDoc-docx" v-html="docContent"></div>

        <div v-if="typeDoc == 'xls' && preview || typeDoc == 'xlsx' && preview" class="AlexiconDoc-xlsx" v-html="docContent"></div>

        <div v-if="typeDoc == 'psd' && preview" class="AlexiconDoc-psd"></div>

        <div v-if="typeDoc == 'ttf' && preview" class="AlexiconDoc-font" :style="`font-family:'${docName.split('.')[0]}';`">
            <div v-html="fontStyle" style="display: none;"></div>
            <p>0123456789.:,;*'"¡!¿?(){}[]/\_-+=^#$%&@°|~`´</p>
            <p>THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.</p>
            <p>The quick brown fox jumps over the lazy dog.</p>
            <p>EL VELOZ MURCIÉLAGO HINDÚ COMÍA FELIZ CARDILLO Y KIWI.</p>
            <p>El veloz murciélago hindú comía feliz cardillo y kiwi.</p>
        </div>

        <div v-if="typeDoc == 'html' && preview || typeDoc == 'htm' && preview" class="AlexiconDoc-html">
            <iframe class="pdf" :src="src" width="100%"></iframe>
        </div>

        <div v-if="openingAsPlain.includes(typeDoc) && preview" class="AlexiconDoc-plain">
            <AlexiconCode :val="docContent"/>
        </div>

        <div v-if="(typeDoc == 'mp4' || typeDoc == 'webm' || typeDoc == 'ogg') && preview" class="AlexiconDoc-video">
            <AlexiconMedia :styles="styles" :type="'video'" :src="src"/>
        </div>

    </div>
</template>

<script>
import mammoth from "mammoth";
import * as XLSX from 'xlsx';
import AlexiconCode from "./AlexiconCode.vue";
import AlexiconMedia from "./AlexiconMedia.vue";
import { Eye, Download, File, FileText, Sheet, CaseSensitive, FileCode, Video, Music, CodeXml, Braces, Terminal } from 'lucide-vue-next';

export default {
    name: 'AlexiconDoc',
    components:{
        AlexiconCode,
        AlexiconMedia,
        Eye, Download, File
    },
    props:{
        styles: Object,
        src: String,
    },
    data(){
        const openingAsPlain = [
            "txt", "xml", "csv", "py", "cpp", "js", "css", "json", "bat"
        ];
        return{
            typeDoc: '',
            docContent: '',
            docName: '',
            preview: false,
            keyUpdater: 0,
            openingAsPlain: openingAsPlain,
            previewAvailableFormats: [
                "pdf", "docx", "xls", "xlsx", "ttf", "html", "htm", "mp4", "webm", "ogg",
                ...openingAsPlain
            ],
            docData: {},
        }
    },
    methods:{
        vibrate(pattern_){
            this.$parent.vibrate(pattern_);
        },

        async renderDocx() {
            try {
                const response = await fetch(this.src);
                const arrayBuffer = await response.arrayBuffer();
                const result = await mammoth.convertToHtml({ arrayBuffer });
                this.docContent = result.value;
            } catch (error) {
                console.error("Error al convertir el DOCX:", error);
            }
        },
        
        async renderExcel() {
            try {
                const response = await fetch(this.src);
                const data = await response.arrayBuffer();
                const workbook = XLSX.read(data, { type: "array" });
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
                const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
                let tableHTML = '<table cellspacing="0" cellpadding="0"><thead><tr>';
                tableHTML += jsonData[0].map(header => `<th>${header}</th>`).join("") + "</tr></thead><tbody>";
                for (let i = 1; i < jsonData.length; i++) {
                    tableHTML += "<tr>";
                    tableHTML += jsonData[i].map(cell => `<td>${cell}</td>`).join("");
                    tableHTML += "</tr>";
                }
                tableHTML += "</tbody></table>";
                this.docContent = tableHTML;
            } catch (error) {
                console.error("Error al procesar el archivo Excel:", error);
            }
        },

        setFontStyle() {
            const fontName = this.docName.split('.')[0];
            const font = new FontFace(fontName, `url(${this.src})`);
            font.load().then(function (loadedFont) {
                document.fonts.add(loadedFont);
            }).catch(function (error) {
                console.error('Error al cargar la fuente:', error);
            });
        },

        readAsPlain(){
            fetch(this.src)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al obtener el archivo');
                    }
                    return response.text();  // Leer el archivo como texto
                })
                .then(fileContent => {
                    this.docContent = fileContent;
                })
                .catch(error => {
                    console.error('Hubo un error al cargar el archivo:', error);
                });
        },

        renderByFormat(){
            const typeDoc = this.typeDoc;

            if(this.docData[typeDoc].render != undefined){
                console.log("is undef")
                this.docData[typeDoc].render();
            }

            this.preview = true;
            this.keyUpdater++;
        },
    },
    mounted() {
        this.typeDoc = this.doc?.toLowerCase() || this.src.split('.').pop().toLowerCase();
        this.docName = this.src.split('/').pop();
        this.docData = {
            "pdf": {icon: FileText, render: undefined},
            "docx": {icon: FileText, render: this.renderDocx},
            "xls": {icon: Sheet, render: undefined},
            "xlsx": {icon: Sheet, render: this.renderExcel},
            "ttf": {icon: CaseSensitive, render: this.setFontStyle},
            "html": {icon: FileCode, render: undefined},
            "htm": {icon: FileCode, render: undefined},
            "mp4": {icon: Video, render: undefined},
            "webm": {icon: Video, render: undefined},
            "ogg": {icon: Music, render: undefined},
            "txt": {icon: FileText, render: this.readAsPlain},
            "xml": {icon: CodeXml, render: this.readAsPlain},
            "csv": {icon: FileCode, render: this.readAsPlain},
            "py": {icon: FileCode, render: this.readAsPlain},
            "cpp": {icon: FileCode, render: this.readAsPlain},
            "js": {icon: Braces, render: this.readAsPlain},
            "css": {icon: Braces, render: this.readAsPlain},
            "json": {icon: Braces, render: this.readAsPlain},
            "bat": {icon: Terminal, render: this.readAsPlain},
        };
    }
}
</script>

<style scoped>
.AlexiconDoc-MAIN{
    width: calc(100% - 4px);
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 5px;
    overflow: hidden;
    border: 2px solid light-dark(v-bind('styles.light.doc.label'), v-bind('styles.dark.doc.label'));
}

.AlexiconDoc-MAIN > *{
    width: 100%;
    max-width: 100%;
}

.AlexiconDoc-MAIN > div:first-child{
    width: calc(100% - 1ch);
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    text-align: center;
    font-size: 1.5ch;
    padding: 0.5ch;
    background-color: light-dark(v-bind('styles.light.doc.label'), v-bind('styles.dark.doc.label'));
    color: light-dark(v-bind('styles.light.doc.txt'), v-bind('styles.dark.doc.txt'));
}

.AlexiconDoc-MAIN > div:first-child span{
    font-size: 1.2ch;
}

.AlexiconDoc-MAIN > div:first-child > div:first-child{
    margin-right: 2ch;
    pointer-events: none;
}

.AlexiconDoc-MAIN .Alexicon-icon-btn{
    margin-left: 3px;
    cursor: pointer;
}

.AlexiconDoc-MAIN .Alexicon-icon-btn > *{
    margin-bottom: -3px;
}

.AlexiconDoc-MAIN > div:not(:first-child):not(.AlexiconDoc-html){
    background-color: red;
    background-color: light-dark(rgba(128, 128, 128, 0.1), rgba(128, 128, 128, 0.2));
}

.AlexiconDoc-pdf{
    aspect-ratio: 2/1 !important;
}

.AlexiconDoc-pdf > div{
    width: 100%;
    height: 100%;
}

.AlexiconDoc-pdf object{
    width: 100%;
    height: 100%;
}

.AlexiconDoc-pdf iframe{
    height: 100%;
}

.AlexiconDoc-docx{
    overflow: auto;
    aspect-ratio: 2/1 !important;
    color-scheme: light;
    background-color: white !important;
    color: black;
}

.AlexiconDoc-docx >>> *{
    max-width: 100%;
    color-scheme: light;
}

.AlexiconDoc-xlsx{
    overflow: auto;
    aspect-ratio: 2/1 !important;
    font-size: 1.25ch;
}

.AlexiconDoc-xlsx >>> *{
    white-space:nowrap;
    border: 1px dotted #089308;
}

.AlexiconDoc-xlsx >>> table{
    border: 0;
}

.AlexiconDoc-xlsx >>> tr{
    height: 0;
    border: 0;
}

p {
    position: absolute;
    color: white;
}

.AlexiconDoc-font{
    display: flex;
    flex-direction: column;
    height: fit-content;
    position: relative;
    padding: 0.5ch 0;
}

.AlexiconDoc-font p{
    position: relative;
    margin: 0;
    text-align: center;
    color: light-dark(v-bind('styles.light.doc.txt'), v-bind('styles.dark.doc.txt'));
    font-family: unset;
}

.AlexiconDoc-html{
    aspect-ratio: 2/1 !important;
}

.AlexiconDoc-html > iframe{
    width: 100%;
    height: 100%;
    border: none;
}

.AlexiconDoc-plain{
    height: fit-content;
    max-height: 30ch;
}

.AlexiconDoc-plain > *{
    width: 100%;
    height: 100%;
}
</style>