<template>
    <section ref="postCreator_MAIN">
        <div class="postCreator-input">

            <div class="postCreator-title">Create post <button class="post-creator-close-button" @click="switchPostCreator(false)">+</button></div>
            
            <div class="postCreator-text">
                <textarea ref="postCreatorTextarea" @keyup="validateTextarea()"  oninput="this.style.height = ''; this.style.height = this.scrollHeight +'px'"></textarea>
                <div class="postCreator-markdown-preview" v-if="preview">
                    <MarkdownRenderer :postId="fakeId" :text="inputText"/>
                </div>
            </div>

            <div class="postCreator-input-media-preview">
                <!-- Mostrar imágenes o videos aquí -->
                <div>
                <div v-for="(file, index) in selectedFiles" :key="index">
                    <img v-if="isImage(file)" :src="getURLfile(file)" alt="Image" />
                    <video v-else-if="isVideo(file)" controls>
                        <source :src="getURLfile(file)+'#t=1'" type="video/mp4" />
                        Tu navegador no admite la reproducción de videos.
                    </video>
                </div>
                </div>
            </div>

            <div>
                <div class="postCreator-btngroup">
                    <button class="postCreator-btn-files">📷
                        <input type="file" ref="fileInput" @change="handleMediaUpload" accept="image/*,video/*" multiple>
                    </button>
                    <button class="postCreator-btn-delete-files" @click="clearMedia()">🗑️</button>
                    <div>
                        <button class="postCreator-btn-preview">
                            <label class="switch">
                                <input type="checkbox" ref="postCreatorNSFW"/>
                                <span class="slider"></span>
                                <div class="switch-bg"></div>
                            </label>
                            &nbsp; NSFW
                        </button>
                        <button class="postCreator-btn-preview">
                            <label class="switch">
                                <input type="checkbox" ref="postCreatorPrivate"/>
                                <span class="slider"></span>
                                <div class="switch-bg"></div>
                            </label>
                            &nbsp; Private post
                        </button>
                        <button class="postCreator-btn-preview">
                            <label class="switch" @click="previewTextareaRender">
                                <input type="checkbox" ref="postCreatorPreviewBtn" @click.stop/>
                                <span class="slider"></span>
                                <div class="switch-bg"></div>
                            </label>
                            &nbsp; Preview
                        </button>
                    </div>
                </div>
                <button class="postCreator-btn-post" ref="postCreatorPostBtn" @click="publishPost">Post</button>
            </div>

        </div>
    </section>
</template>

<script>
import MarkdownRenderer from './postViewer/MarkdownRenderer.vue';

export default {
    name: 'PostCreator',
    components: { MarkdownRenderer },
    data() {
        return {
            inputText: "",
            preview: false,
            selectedFiles: [],
            fakeId: new Date().toLocaleString().replaceAll("/","").replaceAll(" ","").replaceAll(",","").replaceAll(":","")
        };
    },
    methods: {
        handleMediaUpload() {
            const files = this.$refs.fileInput.files;
            // Filtrar solo imágenes o videos válidos
            const validFiles = Array.from(files).filter((file) => this.isValidFileType(file));
            // Agregar los archivos válidos a selectedFiles
            this.selectedFiles = [...this.selectedFiles, ...validFiles];
            // Limpiar el input file para permitir múltiples selecciones
            this.$refs.fileInput.value = '';
            console.log(this.selectedFiles);
        },

        isImage(file) {
            return file.type.startsWith('image/');
        },

        isVideo(file) {
            return file.type.startsWith('video/');
        },

        isValidFileType(file) {
            return this.isImage(file) || this.isVideo(file);
        },

        getURLfile(file_) {
            return URL.createObjectURL(file_);
        },

        validateTextarea() {
            this.inputText = this.$refs.postCreatorTextarea.value;
            if (this.inputText.trim().length > 0) {
                this.$refs.postCreatorPostBtn.classList.add("activated-btn-post");
            }
            else {
                this.$refs.postCreatorPostBtn.classList.remove("activated-btn-post");
            }
        },

        previewTextareaRender() {
            this.preview = !this.$refs.postCreatorPreviewBtn.checked;
        },

        clearMedia() {
            this.selectedFiles = [];
            this.$refs.fileInput.value = '';
        },

        switchPostCreator(mode_){
            this.$parent.switchPostCreator(mode_);
        },

        publishPost() {
            function getCurrentDateTime() {
                const now = new Date();
                const year = now.getFullYear();
                const month = (now.getMonth() + 1).toString().padStart(2, '0');
                const day = now.getDate().toString().padStart(2, '0');
                const hours = now.getHours().toString().padStart(2, '0');
                const minutes = now.getMinutes().toString().padStart(2, '0');
                return `${year}-${month}-${day}-${hours}-${minutes}`;
            }

            function renameFileWithTimestamp(file) {
                const timestamp = getCurrentDateTime();
                // eslint-disable-next-line
                const fileExtension = file.name.split('.').pop(); // Obtiene la extensión del archivo
                const newFileName = `${timestamp}-${file.name}`;
                return new File([file], newFileName, { type: file.type });
            }

            const isNSFW = this.$refs.postCreatorNSFW.checked ? 1 : 0;
            const isPrivate = this.$refs.postCreatorPrivate.checked ? 1 : 0;
            const content = this.inputText;
            const mediaFiles = this.selectedFiles; // Obtén los archivos seleccionados

            if (content == "") {
                return;
            }

            const formData = new FormData();
            formData.append("content", content);
            formData.append("privatePost", isPrivate);
            formData.append("nsfwPost", isNSFW);
            formData.append("shareId", 0);

            // Itera sobre los archivos seleccionados y agrégalos al formData
            for (let i = 0; i < mediaFiles.length; i++) {
                const file = mediaFiles[i];
                const renamedFile = renameFileWithTimestamp(file);
                formData.append("media", renamedFile);
            }

            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT + "/post", {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);
                if(data.status == "ok"){
                    this.$refs.postCreator_MAIN.style.opacity = 0;
                    setTimeout(() => {
                        this.switchPostCreator(false);
                    }, 300);    
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }


    },
}
</script>

<style scoped>
section {
    width: 100%;
    height: calc(100vh - 6ch);
    display: flex;
    justify-content: center;
    position: fixed;
    overflow: auto;
    top: 6ch;
    padding-bottom: 6ch;
    left: 0;
    background-color: rgba(0, 0, 0, 0.75);
    transition: opacity 0.3s;
}

.postCreator-title{
    margin-bottom: 1ch;
}

.postCreator-title > button{
    font-weight: bolder;
    width: 1ch;
    height: 1ch;
    font-size: 3ch;
    transform: rotate(45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background-color: transparent;
    border: none;
    color: gray;
    transition: all 0.1s;
}

.postCreator-title > button:hover{
    cursor: pointer;
    color: lightgray;
    transition: all 0.2s;
}

/* input */
.postCreator-input{
    width: fit-content !important;
    min-width: 512px;
    max-width: calc(100vw - 20ch) !important;
    height: fit-content;
    display: flex;
    flex-direction: column;
    padding: 2ch;
    border-radius: 2ch;
    width: calc(100% - 4ch);
    background-color: rgb(52, 53, 56);
    box-shadow: 0ch 0ch 2ch rgba(0, 0, 0, 0.5);
    margin-top: 6ch;
    margin-bottom: 6ch;
}

/* previewer */
.postCreator-input-media-preview{
    display: flex;
    align-items: center;
    overflow-y: hidden;
    overflow-x: auto;
    margin-bottom: 1ch;
    width: fit-content;
    align-self: center;
    max-width: 100%;
}

.postCreator-input-media-preview > div{
    display: flex;
    align-items: center;
    justify-content: center;
    height: fit-content;
    width: fit-content;
}

.postCreator-input-media-preview > div img, .postCreator-input-media-preview > div video{
    height: 100px;
    border-radius: 1ch;
    margin: 0 1ch;
}

/* textarea and buttons */
.postCreator-text{
    width: 100%;
    height: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-bottom: 1ch;
}

.postCreator-input > .postCreator-text textarea{
    resize: vertical;
    border: none;
    /*border-bottom: 1px solid lightgray;*/
    background-color: transparent;
    background-color: rgba(0, 0, 0, 0.2);
    color: white;
    padding: 1ch;
    width: calc(100% - 2ch);
    border-radius: 1ch;
    scrollbar-width: thin;
    scrollbar-color: rgb(145, 145, 145) rgb(50,50,50);
}

.postCreator-input > .postCreator-text textarea:focus{
    outline: none;
}

.postCreator-markdown-preview{
    width: 100%;
    margin-top: 1ch;
    font-family: sans-serif;
    font-size: 0.8em;
}

.postCreator-input > div{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.postCreator-btngroup{
    display: flex;
    align-items: center;
}

.postCreator-btn-files, .postCreator-btn-delete-files, .postCreator-btn-post, .postCreator-btn-preview{
    position: relative;
    padding: 0.5ch 1ch;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: 0.3ch;
}

.postCreator-btn-files, .postCreator-btn-delete-files{
    background-color: transparent;
    text-shadow: -1px 1px 0 white,
                1px 1px 0 white,
                1px -1px 0 white,
                -1px -1px 0 white;
    font-size: 2.2ch;
}

.postCreator-btn-delete-files{
    font-size: 2ch;
}

.postCreator-btn-preview{
    margin-left: 2ch;
    display: flex;
    align-items: center;
}

.postCreator-btn-preview .switch{
    margin-bottom: -0.2ch;
    cursor: pointer;
}

.postCreator-btn-post, .postCreator-btn-preview{
    background-color: transparent;
    color: gray;
}

.activated-btn-post{
    color: aqua;
}

.activated-btn-post:hover{
    background-color: aqua;
    color: black;
    cursor: pointer;
}

.postCreator-input input[type=file]{
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

    .postCreator-input{
        min-width: unset !important;
        max-width: unset !important;
        width: 85vw !important;
        margin-top: 2ch;
    }

}
</style>