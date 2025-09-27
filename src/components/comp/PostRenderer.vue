<template>
    <section :class="`PostRenderer-MAIN PostRenderer-${postData.id}`" :id="`PostRenderer-${postData.id}`" data-aos="fade-down">

        <div class="PostRenderer-head">
            <a :href="getFrontURL()+'/profile/'+postDataData.owner_id">
                <ImageProtected :mediaId="postDataData?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
            </a>
            <div>
                <p><a :href="getFrontURL()+'/profile/'+postDataData.owner_id">{{ postDataData.name }} {{postDataData.surname}}</a></p>
                <p><a :href="getFrontURL()+'/post/'+postDataData.id">{{ postDataData.post_date }}</a></p>
                <p v-if="postDataData.ai_generated == 1" class="ai-gen-label"><Bot class="ai-gen-icon"/> AI generated</p>
            </div>
        </div>

        <AlexiconComponent :type="'markdown'" :val="postDataData?.content || ''"/>

        <!-- media -->
        <AlexiconComponent :type="'masonry'" :media="filteredMedia.multimedia" :colsNum="3" v-if="filteredMedia.multimedia.length > 0" :key="keyUpdater"/>
        <div v-if="filteredMedia.files.length > 0" :key="keyUpdater">
            <AlexiconComponent :type="'doc'" v-for="(item, index) in filteredMedia.files" :key="index" :val="item" class="PostRenderer-doc"/>
        </div>

        <!-- post shared -->
        <div class="PostRenderer-shared" v-if="typeof postData.share_id == 'number' && postData.share_id > 0 && sharedData.contentLoaded && !shared">
            <a :href="getFrontURL()+'/post/'+sharedData?.content?.id">
                <PostRenderer :postData="sharedData?.content" :shared="true"/>
            </a>
        </div>

        <!-- votes -->
        <div class="PostRenderer-votes" :key="keyUpdater" v-if="!shared"><!--up, down, heart, share, options-->
            <div @click="vote('up')">
                <div><ArrowBigUp :color="postDataData.list_vote_up.includes(AlexiconUserData?.userData?.id) ? '#2ecc71' : ''"/></div>
                <p>{{ postDataData?.list_vote_up?.length }}</p>
            </div>
            <div @click="vote('down')">
                <div><ArrowBigDown :color="postDataData.list_vote_down.includes(AlexiconUserData?.userData?.id) ? '#cb4335' : ''"/></div>
                <p>{{ postDataData?.list_vote_down?.length }}</p>
            </div>
            <div @click="vote('heart')">
                <div class="vote-heart"><Heart :color="postDataData.list_vote_heart.includes(AlexiconUserData?.userData?.id) ? '#ff0000' : ''"/></div>
                <p>{{ postDataData?.list_vote_heart?.length }}</p>
            </div>
            <div @click="share.active = true">
                <div><Forward :color="postDataData.shared_by_list.includes(AlexiconUserData?.userData?.id) ? '#2ecc71' : ''"/></div>
                <p>{{ postDataData?.shared_by_list?.length }}</p>
            </div>
            <div @click="statisticsActive = true">
                <div><UserSearch/></div>
            </div>
            <div @click="optionsActive = true">
                <div><Ellipsis/></div>
            </div>
        </div>

        <!-- view comments -->
        <div class="PostRenderer-view-comments" v-if="!shared">
            <button @click="listComments()">Load {{ postDataData.comment_count }} comments</button>
            <CommentRenderer v-for="(item, index) in commentList" :key="index" :commentData="item"/>
        </div>

        <!-- commentbox -->
        <div class="PostRenderer-commentbox" v-if="!shared">
            <AlexiconComponent :type="'textarea'" @get-val="(val) => commentInputs.text = val" :resize="true" :placeholder="'Comment...'" :key="keyUpdater"/>
            <div class="PostRenderer-commentbox-images">
                <div>
                    <div v-for="(item, index) in commentInputs.media" :key="index">
                        <img v-if="item.type.includes('image/')" :src="item.url">
                        <video v-if="item.type.includes('video/')">
                            <source :src="item.url+'#t=1'" :type="item.type">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                </div>
                <div>
                    <div v-for="(item, index) in commentInputs.media" :key="index">
                        <div v-if="!item.type.includes('image/') && !item.type.includes('video/')">
                            <File/>&nbsp;{{ item.name }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="PostRenderer-commentbox-buttons">
                <div class="lucide-icon"><Paperclip/><input type="file" multiple @change="setFilesPreview()" ref="comment-files-input" accept="image/*,video/*"></div>
                <div class="lucide-icon"><Trash2 @click="deleteFiles()"/></div>
                <label>
                    <AlexiconComponent :type="'switch'" @get-val="(val) => commentInputs.aiGenerated = val" :key="keyUpdater"/> AI generated
                </label>
                <button :disabled="commentInputs.text.trim() == ''" class="highlighted-btn" @click="comment()">Comment</button>
            </div> 
        </div>

    </section>

    <!-- share window -->
    <main class="PostRenderer-share-MAIN" v-if="share.active && !shared">
        <section>
            <div class="PostCreator-close" @click="share.active = false"><X/></div>
            <h1>Share post</h1>
            <AlexiconComponent :type="'textarea'" @get-val="(val) => share.val = val" :resize="true" :placeholder="'Comment...'"/>
            <div class="PostRenderer-share-buttons">
                <div>
                    <label>
                        <AlexiconComponent :type="'switch'" @get-val="(val) => share.privatePost = val"/> Private
                    </label>
                    <label>
                        <AlexiconComponent :type="'switch'" @get-val="(val) => share.nsfwPost = val"/> NSFW
                    </label>
                    <label>
                        <AlexiconComponent :type="'switch'" @get-val="(val) => share.aiGenerated = val"/> AI generated
                    </label>
                </div>
                <button class="highlighted-btn" @click="sharePost()">Share</button>
            </div>
        </section>
    </main>

    <!-- statistics n options -->
    <StatisticsViewer v-if="statisticsActive" :entityData="postData" @close="statisticsActive = false"/>
    <OptionsViewer v-if="optionsActive" :entityData="postData" @close="optionsActive = false"/>

</template>

<script>
import { Paperclip, Trash2, ArrowBigUp, ArrowBigDown, Heart, Forward, UserSearch, Ellipsis, X, Bot } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import CommentRenderer from './CommentRenderer.vue';
import PostRenderer from './PostRenderer.vue';
import StatisticsViewer from './StatisticsViewer.vue';
import OptionsViewer from './OptionsViewer.vue';
import AOS from 'aos'
import 'aos/dist/aos.css'
import ImageProtected from './ImageProtected.vue';

export default {
    name: 'PostRenderer',
    components: {
        AlexiconComponent, CommentRenderer, StatisticsViewer, OptionsViewer, Paperclip, Trash2, ArrowBigUp, ArrowBigDown, Heart, Forward, UserSearch, Ellipsis, X, PostRenderer, Bot, ImageProtected
    },
    props: {
        postData: Object,
        shared: Boolean,
    },
    data(){
        return{
            AlexiconUserData: {},
            postDataData: {},
            commentInputs: {
                text: "",
                media: [],
                aiGenerated: false,
            },
            filteredMedia: {
                multimedia: [],
                files: []
            },
            uploading: false,
            uploadedFilesArray: [],
            keyUpdater: 0,
            commentList: [],
            searchNewComment: 0,
            share: {
                active: false,
                val: '',
                privatePost: false,
                nsfwPost: false,
                aiGenerated: false,
            },
            sharedData: {
                isShared: false,
                content: {},
                contentLoaded: false,
            },
            statisticsActive: false,
            optionsActive: false,
        }
    },
    methods: {
        cleanupFilteredMediaBlobs() {
            for (const it of this.filteredMedia.multimedia) {
                const u = (it && typeof it === 'object') ? it.url : it;
                if (typeof u === 'string' && u.startsWith('blob:')) URL.revokeObjectURL(u);
            }
            for (const it of this.filteredMedia.files) {
                const u = (it && typeof it === 'object') ? it.url : it;
                if (typeof u === 'string' && u.startsWith('blob:')) URL.revokeObjectURL(u);
            }
        },
        
        async filterMedia() {
            // 1) limpiar blobs de una corrida anterior
            this.cleanupFilteredMediaBlobs();
            this.filteredMedia.multimedia = [];
            this.filteredMedia.files = [];

            // 2) normalizar ids (array o string JSON)
            let ids = [];
            const raw = this.postDataData?.media;
            if (Array.isArray(raw)) ids = raw;
            else if (typeof raw === 'string' && raw.trim()) {
                try { ids = JSON.parse(raw); } catch { ids = []; }
            }

            // filtrar valores no numéricos / nulos
            ids = ids.filter(id => Number.isFinite(+id));

            if (!ids.length) return;

            // 3) resolver todos con tu helper
            const endpoint = this.$ENDPOINT;
            const token = this.TOKEN?.();
            const results = await Promise.all(
                ids.map(id => this.alexicon_MEDIA_FILE(endpoint, token, id).catch(() => null))
            );

            // 4) clasificar por tipo
            for (const it of results) {
                if (!it || !it.type) continue;
                if (it.type.startsWith('image/') || it.type.startsWith('video/')) {
                    this.filteredMedia.multimedia.push(it);   // { url (blob), type, filename, isBlob:true }
                } else {
                    this.filteredMedia.files.push(it);        // docs, audio, pdf, etc.
                }
            }
        },

        getFrontURL(){
			return window.location.origin;
		},

        setFilesPreview(){
            const input = this.$refs["comment-files-input"];
            const files = input.files;

            for (let file of files) {
                const fileType = file.type;

                const isMedia = fileType.startsWith("image/") || fileType.startsWith("video/");

                this.commentInputs.media.push({
                    file: file,
                    url: isMedia ? URL.createObjectURL(file) : null,
                    type: fileType,
                    isMedia: isMedia,
                    name: file.name
                });

                if(this.commentInputs.media.length >= 50){
                    return;
                }
            }
        },

        deleteFiles() {
            if(this.uploading) return;
            const input = this.$refs["comment-files-input"];
            if (input) {
                input.value = "";
                this.commentInputs.media = [];
            }
        },

        comment(){
            this.uploading = true;
            const files = this.commentInputs.media.map(item => item.file);
            const numFiles = files.length;

            if (numFiles === 0) return this.finallyComment();

            console.log("TOTAL DE ARCHIVOS A SUBIR:", numFiles)

            const token = this.AlexiconUserData.token;
            const targetPath = `yipnet/${this.AlexiconUserData.userData.id}/`;
            const visibility = this.privatePost ? 'private' : 'public';

            const uploadPromises = Array.from(files).map(file => {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('targetPath', targetPath);
                formData.append('visibility', visibility);

                return fetch(`${this.$ENDPOINT}/alexicon/upload`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                })
                .then(res => res.json());
            });

            Promise.all(uploadPromises)
                .then(results => {
                    console.log("Todos los archivos subidos:", results);
                    for(let i of results){
                        this.uploadedFilesArray.push(i.fileId);
                    }
                    this.finallyComment();
                })
                .catch(err => {
                    console.error("Error al subir uno o más archivos:", err);
                    alert("Error al subir archivos.");
                    this.uploading = false;
                });
        },

        async finallyComment(){
            const newComment = {
                postId: this.postDataData.id,
                content: this.commentInputs.text,
                media: this.uploadedFilesArray,
                aiGenerated: this.commentInputs.aiGenerated,
            };

            const result = await this.yipnet_COMMENT(this.$ENDPOINT, this.TOKEN(), newComment);
            if(result.status == 'ok'){
                console.log("Regenerando this.commentInputs")
                this.commentInputs = {
                    text: "",
                    media: [],
                    aiGenerated: false,
                };
                this.uploadedFilesArray = [];
                this.keyUpdater++;
                this.searchNewComment = result.comment_id;
                this.listComments();
            }
            this.uploading = false;
            this.searchNewComment = 0;
        },

        async listComments(){
            const result = await this.yipnet_LIST_COMMENTS(this.$ENDPOINT, this.TOKEN(), this.postDataData.id);

            if (result.response) {
                console.error("Error del servidor:", result.response);
            } else {
                this.commentList = result.comment_list;
                if(this.autoTargetComment()){
                    this.$nextTick(() => document.getElementById(this.autoTargetComment()).scrollIntoView() );
                }
                if(this.searchNewComment == 0) return;
                this.$nextTick(() => {
                    document.getElementById(`CommentRenderer-${this.searchNewComment}`).scrollIntoView();
                    this.searchNewComment = 0;
                });
            }
        },

        async vote(voteType){
            const voteData = {
                voteType,
                targetId: this.postDataData.id,
                entityType: 'post'
            };

            const result = await this.yipnet_VOTE(this.$ENDPOINT, this.TOKEN(), voteData);

            console.log("Resultado de la votación:", result);
            if(result.response != "Vote updated"){ return; }
            if(result.status == "added"){
                if(!this.postDataData[`list_vote_${voteType}`].includes(this.AlexiconUserData.userData.id)){
                    this.postDataData[`list_vote_${voteType}`].push(this.AlexiconUserData.userData.id);
                }
            }else
            if(result.status == "removed"){
                const index = this.postDataData[`list_vote_${voteType}`].indexOf(this.AlexiconUserData.userData.id);
                if(index !== -1) this.postDataData[`list_vote_${voteType}`].splice(index, 1);
            }
            this.keyUpdater++;
        },

        async sharePost(){
            const newPost = {
                content: this.share.val,
                media: JSON.stringify([]),
                shareId: this.postDataData.id,
                privatePost: this.share.privatePost,
                nsfwPost: this.share.nsfwPost,
                aiGenerated: this.share.aiGenerated
            };
            const result = await this.yipnet_POST(this.$ENDPOINT, this.TOKEN(), newPost);
            if(result.response == "Post created successfully.") this.share.active = false;
        },

        async getSinlgePost(id_){
            const result = await this.yipnet_GET_SINGLE_POST(this.$ENDPOINT, this.TOKEN(), id_);
            this.sharedData.content = result;
            this.$nextTick(() => this.sharedData.contentLoaded = true );
        },

        autoTargetComment(){
            let result = window.location.href;
            if(result.includes("#")){
                return result.split("#")[1].trim();
            }
            return false;
        }
    },
    beforeMount(){
        this.postDataData = this.postData;
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.filterMedia();
        console.log("check id shared", this.postDataData.share_id)
        if(typeof this.postData.share_id == 'number' && this.postData.share_id > 0){
            this.getSinlgePost(this.postData.share_id);
        }
        AOS.init();

        if(this.autoTargetComment()){
            this.listComments();
        }
    },
    beforeUnmount() {
        // liberar blobs al salir
        this.cleanupFilteredMediaBlobs();
    },
    watch: {
        postData: {
            deep: true,
            handler(val){
                this.postDataData = val || {};
                this.filterMedia();
            }
        }
    }
}
</script>

<style scoped>
.PostRenderer-MAIN{
    color: light-dark(black, white);
    background-color: light-dark(#f2f2f2, #2d2d2d);
    border-radius: 10px;
    padding: 2ch;
    box-shadow: 0 0 2ch rgba(0, 0, 0, 0.2);
    width: 75ch;
    max-width: calc(100vw - 6ch);
    margin: 0 auto;
    margin-bottom: 4ch;
    overflow-x: hidden;
}

.lucide-icon{
    width: 3ch;
    aspect-ratio: 1/1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.lucide-icon:hover{
    scale: 1.05;
    cursor: pointer;
}

/* head */
.PostRenderer-head{
    display: flex;
    align-items: center;
    height: fit-content;
}

.PostRenderer-head > a{
    display: flex;
    width: 50px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    overflow: hidden;
}

.PostRenderer-head > a > img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.PostRenderer-head > div{
    margin-left: 1ch;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.PostRenderer-head > div > p{
    margin: 0;
}

.PostRenderer-head > div > p:first-child{
    margin-bottom: 0.5ch;
}

.PostRenderer-head > div > p:first-child a{
    color: light-dark(black, white);
}

.PostRenderer-head > div > p:nth-child(2){
    color: gray;
    font-size: 1.5ch;
}

.PostRenderer-head > div > p:nth-child(2) a{
    color: gray;
}

.PostRenderer-head > div > p a{
    text-decoration: none;
}

.PostRenderer-head > div > p a:hover{
    text-decoration: underline;
    cursor: pointer;
}

.ai-gen-label{
    color: gray;
    font-size: 1.4ch;
    margin-top: 0.2ch !important;
    display: flex;
    align-items: center;
}

.ai-gen-icon{
    margin-right: 0.5ch;
    margin-top: -0.5ch;
    scale: 0.9;
}

.PostRenderer-MAIN:deep(.AlexiconDoc-MAIN){
    margin: 1.5ch 0;
}

/* votes */
.PostRenderer-votes{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid rgba(128, 128, 128, 0.25);
    border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    padding: 5px 0;
}

.PostRenderer-votes > div{
    display: flex;
    align-items: center;
    justify-content: center;
    width: fit-content;
}

.PostRenderer-votes > div:hover{
    cursor: pointer;
    scale: 1.1;
}

.PostRenderer-votes > div > div{
    margin-bottom: -5px;
}

.PostRenderer-votes > div p{
    margin: 0;
    margin-left: 5px;
}

.PostRenderer-votes .vote-heart > *{
    scale: 0.75;
}

/* view comments */
.PostRenderer-view-comments{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 10px;
}

.PostRenderer-view-comments > button:first-child{
    min-width: 25%;
    margin-bottom: 10px;
}

/* commentbox */
.PostRenderer-commentbox-buttons{
    margin-top: 1ch;
    display: flex;
    align-items: center;
}

.PostRenderer-commentbox-buttons label{
    display: flex;
    align-items: center;
    margin-right: 3ch;
}

.PostRenderer-commentbox-buttons label:deep(label){
    margin-right: 1ch !important;
}

.PostRenderer-commentbox-buttons .lucide-icon{
    margin-right: 3ch;
}

.PostRenderer-commentbox-buttons button{
    margin-left: auto;
}

.PostRenderer-commentbox-buttons .lucide-icon{
    position: relative;
    cursor: pointer;
}

.PostRenderer-commentbox-buttons .lucide-icon input{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

/* commentbox-images */
.PostRenderer-commentbox-images{
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 100%;
    margin-top: 1ch;
}

.PostRenderer-commentbox-images > div{
    width: fit-content;
    max-width: 100%;
    display: flex;
    align-items: center;
    overflow-x: auto;
}

.PostRenderer-commentbox-images > div img, .PostRenderer-commentbox-images > div video{
    max-width: 100px;
    max-height: 100px;
    border-radius: 5px;
    background-color: rgba(128, 128, 128, 0.25);
    margin: 0 5px;
}

/* share */
.PostRenderer-share-MAIN{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(0,0,0,0.5);
    z-index: 3;
}

.PostRenderer-share-MAIN > section{
    color: light-dark(black, white);
    background-color: light-dark(#f2f2f2, #2d2d2d);
    border-radius: 10px;
    padding: 2ch;
    position: relative;
    display: flex;
    flex-direction: column;
    max-width: 75vw;
    max-height: 75vh;
    min-height: 25vh;
    min-width: 30vw;
}

.PostRenderer-share-MAIN > section > h1{
    margin-top: 0;
}

.PostCreator-close{
    position: absolute;
    top: 1ch;
    right: 1ch;
}

.PostCreator-close:hover{
    cursor: pointer;
    scale: 1.1;
}

.PostRenderer-share-buttons{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
}

.PostRenderer-share-MAIN button{
    width: fit-content;
    margin-left: auto;
}

.PostRenderer-share-buttons > div, .PostRenderer-share-buttons label{
    display: flex;
    align-items: center;
    margin-right: 3ch;
}

.PostRenderer-share-buttons label:deep(label){
    margin-right: 1ch !important;
}

/* shared */
.PostRenderer-shared{
    margin: 2ch 0;
    overflow: hidden;
}

.PostRenderer-shared:hover{
    cursor: pointer;
    scale: 1.01;
    transition: scale 0.1s;
}

.PostRenderer-shared > a{
    text-decoration: unset;
}

.PostRenderer-shared > a >>> .PostRenderer-MAIN{
    pointer-events: none;
    width: 69ch !important;
    max-width: calc(100vw - 12ch) !important;
    border-left: 10px solid light-dark(rgba(128, 128, 128, 0.5), rgba(128, 128, 128, 0.25));
}
</style>