<template> <!-- Aquí estará tanto la caja de texto como la carga de comentarios de los posts-->
    <section>

        <div class="comments-bar">
            <div>
                <button @click="manageVote('Up', 'posts')" ref="voteUpBtn" :class="getVotesClasses('Up')">▲</button>
                {{ votes }}
                <button @click="manageVote('Down', 'posts')" ref="voteDownBtn" :class="getVotesClasses('Down')">▼</button>
            </div>
            <div><button @click="manageVote('Heart', 'posts')" ref="voteHeartBtn" :class="getVotesClasses('Heart')">❤</button> {{ hearts }}</div>
            <div><button @click="shareWindow = true" ref="shareBtn">⤷</button> {{ shares }}</div>
            <div class="comment-btn-post activated-btn-post" @click="toCommentBox()">Comment</div>
        </div>

        <div class="comments-load">
            <!-- "See (num of comments of post) comments" button -->
            <button @click="getComments()" class="load-comments-btn MAIN-BUTTON">See {{ numOfComments }} comments</button>
            <!-- Un v-for con toda la carga de comentarios. Lo siguiente es solo de ejemplo. -->
            <div v-for="(comment, index) in commentList" :key="index" class="comment-user-info">
                <div class="comment-userimg" v-if="!myBlockedList.includes(comment.comment_owner_id)"
                    :style="`background-image:url('${
                        comment?.user_profile_pic == ''
                        ? require('../assets/images/default-user.jpg')
                        :  this.$ENDPOINT + '/static/users/' + comment.comment_owner_id +'/'+ comment.user_profile_pic
                    }');`
                "></div>
                <div class="comment-contents" v-if="!myBlockedList.includes(comment.comment_owner_id)">
                    <div class="comment-panel">
                        <span v-if="parseInt(myId) == parseInt(comment.comment_owner_id)" class="del-comment">🗑️</span>
                        <span v-else>🚨</span>
                    </div>
                    <p class="comment-username"><a class="comment-username" :href="toProfile(comment.ownerId)">{{ comment.user_name}} {{ comment.user_surname }}</a></p>
                    <p class="comment-date">{{ comment.commentDate }}</p>
                    <div><MarkdownRenderer :postId="postId+comment.comment_id" :text="comment.comment_content"/></div>
                    <MediaDisplayer v-if="comment.comment_media" class="post-media" :images="comment.comment_media" :ownerId="comment.comment_owner_id"/>
                    <div class="comment-votes-panel">
                        <div>
                            <button @click="manageVote('Up', 'comments', comment.comment_id)" :id="`voteUpBtnComment${comment.comment_id}OfPost${this.postId}`" :class="getVotesCommentClasses('Up', comment.voteUp)" style="background-color:transparent!important; border:none!important;">▲</button>
                            <span :id="`voteUpDownTxtComment${comment.comment_id}OfPost${postId}`">{{ JSON.parse(comment.voteUp).length - JSON.parse(comment.voteDown).length }}</span>
                            <button @click="manageVote('Down', 'comments', comment.comment_id)" :id="`voteDownBtnComment${comment.comment_id}OfPost${this.postId}`" :class="getVotesCommentClasses('Down', comment.voteDown)" style="background-color:transparent!important; border:none!important;">▼</button>
                        </div>
                        <div><button @click="manageVote('Heart', 'comments', comment.comment_id)" :id="`voteHeartBtnComment${comment.comment_id}OfPost${this.postId}`" :class="getVotesCommentClasses('Heart', comment.voteHeart)" style="background-color:transparent!important; border:none!important;">❤</button>
                            <span :id="`voteHeartTxtComment${comment.comment_id}OfPost${postId}`">{{ JSON.parse(comment.voteHeart).length }}</span>
                        </div>
                    </div>
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

        <section class="share-post" v-if="shareWindow">
            <div>
                <button @click="shareWindow = false, shareContent = '',sharePreviewTxt = false">+</button>
                <h2>Share</h2>
                <textarea ref="shareContent" placeholder="Write a comment..." v-model="shareContent" oninput="this.style.height = ''; this.style.height = this.scrollHeight +'px'"></textarea>
                <br>
                <MarkdownRenderer :postId="'share-preview'" :text="shareContent" v-if="sharePreviewTxt" class="shareContentRenderer"/>
                <div>
                    <button class="postShare-btn-preview">
                        <label class="switch">
                            <input type="checkbox" v-model="sharePreviewTxt"/>
                            <span class="slider"></span>
                            <div class="switch-bg"></div>
                        </label>
                        &nbsp; Preview
                    </button>
                    <div>
                        <button class="MAIN-BUTTON" @click="share()">Share</button>
                        <button class="MAIN-BUTTON cancel-btn" @click="shareWindow = false, shareContent = '',sharePreviewTxt = false">Cancel</button>
                    </div>
                </div>
            </div>
        </section>

    </section>
</template>

<script>
import MarkdownRenderer from './postViewer/MarkdownRenderer.vue';
import MediaDisplayer from './postViewer/MediaDisplayer.vue';

export default {
    name: 'CommentLayout',
    props: {
        postId: String,
        shareId: Number,
        numOfComments: Number,
        sharedByList: [String, Array],
        allPostData: Object,
    },
    data() {
        return {
            votes: JSON.parse(this.allPostData.voteUp).length - JSON.parse(this.allPostData.voteDown).length,
            hearts: JSON.parse(this.allPostData.voteHeart).length,
            shares: JSON.parse(this.allPostData.sharedByList).length,
            inputText: "",
            preview: false,
            selectedFiles: [],
            commentList: [],
            myId: JSON.parse(localStorage.getItem("yipUserData")).userData.id,
            myBlockedList: JSON.parse(localStorage.getItem("yipUserData")).userData.negativeList,
            shareIdData: 0,
            shareWindow: false,
            shareContent: "",
            sharePreviewTxt: false,
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
                        console.log("listado de comentarios", this.commentList)
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
                    let newComment = data.message.comment;
                    console.log("newComment", newComment);
                    newComment.comment_id = newComment.id;
                    newComment.comment_owner_id = newComment.ownerId;
                    newComment.comment_content = newComment.content;
                    newComment.user_profile_pic = newComment.currentProfilePic;
                    newComment.user_name = newComment.name;
                    newComment.user_surname = newComment.surname;
                    newComment.voteHeart = JSON.stringify(newComment.voteHeart);
                    newComment.voteUp = JSON.stringify(newComment.voteUp);
                    newComment.voteDown = JSON.stringify(newComment.voteDown);
                    this.commentList.push(data.message.comment);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },

        share(){
            const formData = new FormData();
            formData.append("content", this.shareContent);
            formData.append("privatePost", 0);
            formData.append("nsfwPost", 0);
            formData.append("shareId", parseInt(this.postId));

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
                    console.log("shared");
                    this.shareWindow = false;
                    this.shareContent = '';
                    this.sharePreviewTxt = false;
                    this.$refs.shareBtn.class = "already-shared";  
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
        
        manageVote(voteType_, elementType_, commentId_=0) {
            const targetEntityId = elementType_ == "posts" ? parseInt(this.postId) : commentId_; // "posts" | "comments"
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            const formData = new FormData();
            formData.append("targetEntityId", targetEntityId);
            formData.append("voteType", voteType_);
            formData.append("entityType", elementType_);

            fetch(this.$ENDPOINT + "/manage_vote", {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);
                if(data.json.status == "ok"){
                    this.$nextTick(() => {

                        if(data.json.message.response == "Vote removed successfully."){
                            if(elementType_ == "posts"){
                                this.$refs[`vote${voteType_}Btn`].classList.remove(`voted${voteType_}`);
                                if(voteType_ == "Up"){
                                    this.votes -= 1;
                                }else if(voteType_ == "Down"){
                                    this.votes += 1;
                                }else{
                                    this.hearts -= 1;
                                }
                            }else
                            if(elementType_ == "comments"){
                                document.getElementById(`vote${voteType_}BtnComment${commentId_}OfPost${this.postId}`).classList.remove(`voted${voteType_}`);
                                const UpDownTxt = document.getElementById(`voteUpDownTxtComment${commentId_}OfPost${this.postId}`);
                                const HeartTxt = document.getElementById(`voteHeartTxtComment${commentId_}OfPost${this.postId}`);
                                if(voteType_ == "Up"){
                                    UpDownTxt.innerHTML = parseInt(UpDownTxt.innerHTML) - 1;
                                }else if(voteType_ == "Down"){
                                    UpDownTxt.innerHTML = parseInt(UpDownTxt.innerHTML) + 1;
                                }else{
                                    HeartTxt.innerHTML = parseInt(HeartTxt.innerHTML) - 1;
                                }
                            }
                        }else
                        if(data.json.message.response == "Vote added successfully."){
                            if(elementType_ == "posts"){
                                this.$refs[`vote${voteType_}Btn`].classList.add(`voted${voteType_}`);
                                if(voteType_ == "Up"){
                                    this.votes += 1;
                                }else if(voteType_ == "Down"){
                                    this.votes -= 1;
                                }else{
                                    this.hearts += 1;
                                }
                            }else
                            if(elementType_ == "comments"){
                                document.getElementById(`vote${voteType_}BtnComment${commentId_}OfPost${this.postId}`).classList.add(`voted${voteType_}`);
                                const UpDownTxt = document.getElementById(`voteUpDownTxtComment${commentId_}OfPost${this.postId}`);
                                const HeartTxt = document.getElementById(`voteHeartTxtComment${commentId_}OfPost${this.postId}`);
                                if(voteType_ == "Up"){
                                    UpDownTxt.innerHTML = parseInt(UpDownTxt.innerHTML) + 1;
                                }else if(voteType_ == "Down"){
                                    UpDownTxt.innerHTML = parseInt(UpDownTxt.innerHTML) - 1;
                                }else{
                                    HeartTxt.innerHTML = parseInt(HeartTxt.innerHTML) + 1;
                                }
                            }
                        }

                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },

        getVotesClasses(voteType_){
            const voteArr = JSON.parse(this.allPostData[`vote${voteType_}`]);
            if(voteArr.includes(this.myId)){
                return `voted${voteType_}`
            }else{
                return ""
            }
        },

        getVotesCommentClasses(voteType_, arr_){
            try {
                const voteArr = JSON.parse(arr_);
                if(voteArr.includes(this.myId)){
                    return `voted${voteType_}`
                }else{
                    return ""
                }
            } catch (error) {
                return ""
            }
        }

    },
    mounted(){
        if(this.shareId != 0){
            this.shareIdData = this.shareId;
        }
    },
    components: { MarkdownRenderer, MediaDisplayer }
}
</script>

<style scoped>
section{
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

.comments-bar button:hover{
    cursor: pointer;
    color: white;
    text-shadow: 0 0 1ch white;
}

.already-shared{
    color: rgb(54, 255, 47);
    pointer-events: none;
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
  margin: 0;
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
  width: 4.4ch !important;
  height: 4.2ch !important;
  aspect-ratio: 1/1 !important;
  border-radius: 100vw !important;
  background-size: cover;
  margin-right: 1.4ch;
  margin-top: 1.2ch;
  background-position: center;
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

.comment-votes-panel{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-top: 0.5ch;
    font-family: monospace;
}

.comment-votes-panel > div{
    margin-left: 3ch !important;
    scale: 0.9;
}

.comment-votes-panel button{
    border: none;
    background-color: transparent;
    color: gray;
}

.comment-votes-panel button:hover{
    cursor: pointer;
    color: white;
    text-shadow: 0 0 1ch white;
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
    margin-top: 2ch;
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

.share-post{
    width: 100% !important;
    padding: 0;
    height: calc(100vh - 6ch);
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    overflow: auto;
    top: 6ch;
    left: 0;
    background-color: rgba(0, 0, 0, 0.75);
    z-index: 2;
    transition: opacity 0.3s;
}

.share-post > div{
    width: fit-content;
    height: fit-content;
    display: flex;
    flex-direction: column;
    padding: 2ch;
    border-radius: 2ch;
    background-color: rgb(52, 53, 56);
    box-shadow: 0ch 0ch 2ch rgba(0, 0, 0, 0.5);
    position: relative;
    width: 80vw;
    max-width: calc(512px + 2ch);
    min-height: fit-content;
    max-height: 88vh;
    overflow: auto;
}

.share-post > div > button{
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
    position: absolute;
    right: 1ch;
    cursor: pointer;
}

.share-post textarea{
    resize: vertical;
    border: none;
    background-color: rgba(0, 0, 0, 0.2);
    color: white;
    padding: 1ch;
    width: calc(100% - 2ch);
    border-radius: 1ch;
    scrollbar-width: thin;
    scrollbar-color: rgb(145, 145, 145) rgb(50,50,50);
}

.postShare-btn-preview{
    background-color: transparent;
    color: gray;
    position: relative;
    padding: 0.5ch 1ch;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: 0.3ch;
}

label{
    cursor: pointer;
}

.share-post > div > div{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1ch;
}

.shareContentRenderer{
    margin: 1ch 0;
}

.share-post button:not(.postShare-btn-preview){
    margin-left: 2ch;
}

.cancel-btn{
    color: white;
}

.cancel-btn:hover{
    background-color: #686A70;
}

/* vote styles */
.votedUp{
    color: greenyellow !important;
}

.votedDown{
    color: red !important;
}

.votedHeart{
    color: rgb(255, 0, 85) !important;
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

    .share-post > div{
        width: 85vw;
        max-width: unset;
    }

}
</style>