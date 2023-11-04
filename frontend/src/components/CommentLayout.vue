<template> <!-- Aquí estará tanto la caja de texto como la carga de comentarios de los posts-->
    <section>

        <div class="comments-bar">
            <div><button>▲</button> {{ votes }} <button>▼</button></div>
            <div><button>❤</button> {{ hearts }}</div>
            <div><button>⤷</button> {{ shares }}</div>
            <div class="comment-btn-post activated-btn-post"><a :href="`#comments-input-${postId}`">Comment</a></div>
        </div>

        <div class="comments-load">
            <!-- Un v-for con toda la carga de comentarios. Lo siguiente es solo de ejemplo. -->
            <div class="comment-user-info">
                <div class="comment-userimg" :style="`background-image:url('${require('../assets/images/default-user.jpg')}');`"></div>
                <div>
                    <p class="comment-username">Alexa Kitsune</p>
                    <p class="comment-date">20/09/2023 03:12</p>
                </div>
            </div>
        </div>

        <div class="comments-input" :id="`comments-input-${postId}`">
            <div class="comments-text">
                <textarea ref="commentTextarea" @keyup="validateTextarea()" oninput="this.style.height = ''; this.style.height = this.scrollHeight +'px'"></textarea>
                <div class="comment-markdown-preview" v-if="preview">
                    <MarkdownRenderer :postId="postId" :text="inputText"/>
                </div>
            </div>
            <div class="comments-input-media-preview">
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
                <div class="comment-btngroup">
                    <button class="comment-btn-files">📷
                        <input type="file" ref="fileInput" @change="handleMediaUpload" accept="image/*,video/*" multiple>
                    </button>
                    <button class="comment-btn-delete-files" @click="clearMedia()">🗑️</button>
                    <button class="comment-btn-preview">
                        <label class="switch" @click="previewTextareaRender">
                            <input type="checkbox" ref="commentPreviewBtn" @click.stop/>
                            <span class="slider"></span>
                            <div class="switch-bg"></div>
                        </label>
                        &nbsp; Preview
                    </button>

                </div>
                <button class="comment-btn-post" ref="commentPostBtn">Post</button>
            </div>
        </div>

    </section>
</template>

<script>
import MarkdownRenderer from './postViewer/MarkdownRenderer.vue';

export default {
    name: 'CommentLayout',
    props: {
        postId: String,
    },
    data() {
        return {
            votes: 0,
            hearts: 0,
            shares: 0,
            inputText: "",
            preview: false,
            selectedFiles: [],
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
            this.inputText = this.$refs.commentTextarea.value;
            if (this.inputText.trim().length > 0) {
                this.$refs.commentPostBtn.classList.add("activated-btn-post");
            } else {
                this.$refs.commentPostBtn.classList.remove("activated-btn-post");
            }
        },

        previewTextareaRender(){
            this.preview = !this.$refs.commentPreviewBtn.checked;
        },

        clearMedia(){
            this.selectedFiles = [];
            this.$refs.fileInput.value = '';
        },

        getComments(){
            // Get all comments in the array by id. 
        },

        postComment(){

        }
    },
    components: { MarkdownRenderer }
}
</script>

<style scoped>
section
{
    color: white;
    font-family: monospace;
    display: flex;
    flex-direction: column;
    margin-top: 1ch;
    border-radius: 1ch;
    padding: 2ch;
    width: calc(100% - 8ch) !important;
    background-color: rgba(0, 0, 0, 0.2);
}

/* bar */
.comments-bar{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.comments-bar button{
    border: none;
    background-color: transparent;
    color: gray;
}

.comments-bar > div a{
    text-decoration: none;
    font-family: sans-serif;
    font-size: 1em;
    color: unset;
}

.comments-bar > div a:visited{
    color: unset;
}

/* Comments load user info */
.comment-user-info{
  display: flex;
  align-items: center;
  font-family: sans-serif;
  margin: 2ch 0;
}

.comment-userimg{
  width: 4ch;
  height: 4ch;
  border-radius: 100vw;
  background-size: cover;
  margin-right: 1.4ch;
}

.comment-user-info p{
  margin: 0.4ch;
}

.comment-username{
  color: aqua;
}

.comment-date{
  color: gray;
  font-size: 1.4ch;
}

/* input */
.comments-input{
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 2ch;
    border-radius: 2ch;
    width: calc(100% - 4ch);
    background-color: rgb(52, 53, 56);
}

/* previewer */
.comments-input-media-preview{
    display: flex;
    align-items: center;
    overflow-y: hidden;
    overflow-x: auto;
    margin-bottom: 1ch;
    width: fit-content;
    align-self: center;
    max-width: 100%;
}

.comments-input-media-preview > div{
    display: flex;
    align-items: center;
    justify-content: center;
    height: fit-content;
    width: fit-content;
}

.comments-input-media-preview > div img, .comments-input-media-preview > div video{
    height: 100px;
    border-radius: 1ch;
    margin: 0 1ch;
}

/* textarea and buttons */
.comments-text{
    width: 100%;
    height: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-bottom: 1ch;
}

.comments-input > .comments-text textarea{
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

.comments-input > .comments-text textarea:focus{
    outline: none;
}

.comment-markdown-preview{
    width: 100%;
    margin-top: 1ch;
    font-family: sans-serif;
    font-size: 0.8em;
}

.comments-input > div{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.comment-btngroup{
    display: flex;
    align-items: center;
}

.comment-btn-files, .comment-btn-delete-files, .comment-btn-post, .comment-btn-preview{
    cursor: pointer;
    position: relative;
    padding: 0.5ch 1ch;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: 0.3ch;
}

.comment-btn-files, .comment-btn-delete-files{
    background-color: transparent;
    text-shadow: -1px 1px 0 white,
                1px 1px 0 white,
                1px -1px 0 white,
                -1px -1px 0 white;
    font-size: 2.2ch;
}

.comment-btn-delete-files{
    font-size: 2ch;
}

.comment-btn-preview{
    margin-left: 2ch;
    display: flex;
    align-items: center;
}

.comment-btn-preview .switch{
    margin-bottom: -0.2ch;
    cursor: pointer;
}

.comment-btn-post, .comment-btn-preview{
    background-color: transparent;
    color: gray;
}

.activated-btn-post{
    color: aqua;
}

.activated-btn-post:hover{
    background-color: aqua;
    color: black;
}

.comments-input input[type=file]{
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}
</style>