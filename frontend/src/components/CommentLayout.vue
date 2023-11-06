<template> <!-- Aquí estará tanto la caja de texto como la carga de comentarios de los posts-->
    <section>

        <div class="comments-bar">
            <div><button>▲</button> {{ votes }} <button>▼</button></div>
            <div><button>❤</button> {{ hearts }}</div>
            <div><button>⤷</button> {{ shares }}</div>
            <div class="comment-btn-post activated-btn-post" @click="toCommentBox()">Comment</div>
        </div>

        <div class="comments-load">
            <!-- "See (num of comments of post) comments" button -->
            <button @click="getComments()" class="load-comments-btn MAIN-BUTTON">See {{ numOfComments }} comments</button>
            <!-- Un v-for con toda la carga de comentarios. Lo siguiente es solo de ejemplo. -->
            <div v-for="(comment, index) in commentList" :key="index" class="comment-user-info">
                <div class="comment-userimg"
                    :style="`background-image:url('${
                        this.$ENDPOINT + '/static/users/' + comment.comment_owner_id +'/'+ comment.user_profile_pic || require('../assets/images/default-user.jpg')
                    }');`
                "></div>
                <div class="comment-contents">
                    <div class="comment-panel">
                        <span v-if="parseInt(myId) == parseInt(comment.comment_owner_id)" class="del-comment">🗑️</span>
                        <span v-else>🚨</span>
                    </div>
                    <p class="comment-username"><a class="comment-username" :href="toProfile(comment.ownerId)">{{ comment.user_name}} {{ comment.user_surname }}</a></p>
                    <p class="comment-date">{{ comment.commentDate }}</p>
                    <div><MarkdownRenderer :postId="postId+comment.comment_id" :text="comment.comment_content"/></div>
                    <MediaDisplayer v-if="comment.comment_media" class="post-media" :images="comment.comment_media" :ownerId="comment.comment_owner_id"/>
                </div>
            </div>
        </div>

        <div class="comments-input">
            <div class="comments-text">
                <textarea ref="commentTextarea" @keyup="validateTextarea()" oninput="this.style.height = ''; this.style.height = this.scrollHeight +'px'"></textarea>
                <div class="comment-markdown-preview" v-if="preview">
                    <MarkdownRenderer :postId="postId+'_'+postId" :text="inputText"/>
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
                <button class="comment-btn-post" ref="commentPostBtn" @click="publishComment()">Post</button>
            </div>
        </div>

    </section>
</template>

<script>
import MarkdownRenderer from './postViewer/MarkdownRenderer.vue';
import MediaDisplayer from './postViewer/MediaDisplayer.vue';

export default {
    name: 'CommentLayout',
    props: {
        postId: String,
        numOfComments: Number
    },
    data() {
        return {
            votes: 0,
            hearts: 0,
            shares: 0,
            inputText: "",
            preview: false,
            selectedFiles: [],
            commentList: [],
            myId: JSON.parse(localStorage.getItem("yipUserData")).userData.id
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

        toCommentBox(){
            this.$refs.commentTextarea.scrollIntoView();
            this.$refs.commentTextarea.focus();
        },

        getComments(){
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/comment_list/" + this.postId, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + token // Donde "token" es el token de autorización que deseas enviar
                }})
                .then(response => response.json())
                .then(data => {
                    if(data.status == "ok"){
                        this.commentList = data.message.comment_list;
                    }
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        },

        toProfile(id_){
            const profileUrl = window.location.href.split("#")[0];
            return profileUrl + "#/profile~" + id_ ;
        },

        publishComment() {
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

            const content = this.inputText;
            const mediaFiles = this.selectedFiles; // Obtén los archivos seleccionados

            console.log(content, mediaFiles)

            if (content == "") {
                return;
            }

            const formData = new FormData();
            formData.append("content", content);

            // Itera sobre los archivos seleccionados y agrégalos al formData
            for (let i = 0; i < mediaFiles.length; i++) {
                const file = mediaFiles[i];
                const renamedFile = renameFileWithTimestamp(file);
                formData.append("media", renamedFile);
            }

            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT + "/comment/" + this.postId, {
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
                    this.inputText = "";
                    this.$refs.commentTextarea.value = "";
                    this.$refs.commentTextarea.style.height = "fit-content";
                    this.clearMedia();   
                    console.log("DATA created:", data.message.comment)
                    this.commentList.push(data.message.comment);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
    },
    components: { MarkdownRenderer, MediaDisplayer }
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
.comments-load{
    display: flex;
    flex-direction: column;
    max-width: 485px;
}

.comment-user-info{    
  display: flex;
  position: relative;
  font-family: sans-serif;
  margin: 2ch 0;
}

.comment-panel{
    width: 100%;
    text-align: right;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    justify-self: flex-end;
    align-self: flex-end;
}

.comment-panel span:not(.del-comment){
    opacity: 0.5;
    filter: grayscale(1);
}

.comment-panel span:hover{
    opacity: 1;
    cursor: pointer;
    filter: grayscale(0);
}

.del-comment{
    opacity: 0.5;
    filter: grayscale(0.5);
}

.comment-userimg{
  width: 5ch !important;
  height: 5ch !important;
  aspect-ratio: 1 / 1;
  border-radius: 100vw;
  background-size: cover;
  margin-right: 1.4ch;
}

.comment-user-info p{
  margin: 0.4ch;
}

.comment-contents{
    display: flex;
    flex-direction: column;
    width: 100%;
}

.comment-username{
  color: aqua !important;
  text-decoration: none;
}

.comment-username:hover{
    text-decoration: underline;
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

.load-comments-btn{
    border: none;
    border-radius: 0.5ch;
    margin: 1ch 0;
    padding: 0.5ch 0;
    background-color: transparent;
    cursor: pointer;
    margin-left: 1%;
}

/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

    .comments-load{
        max-width: unset;
    }

    .load-comments-btn{
        margin-left: 0;
    }

}
</style>