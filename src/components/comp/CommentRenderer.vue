<template>
    <div :class="`CommentRenderer-MAIN CommentRenderer-${commentData.id}`" :id="`CommentRenderer-${commentData.id}`" data-aos="fade-left">

        <div class="CommentRenderer-head">
            <a :href="getFrontURL()+'/profile/'+commentDataData.owner_id">
                <ImageProtected :mediaId="commentDataData?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
            </a>
            <div>
                <p><a :href="getFrontURL()+'/profile/'+commentDataData.owner_id">{{ commentDataData.name }} {{commentDataData.surname}}</a></p>
                <p>{{ commentDataData.comment_date }}</p>
                <p v-if="commentDataData.ai_generated == 1" class="ai-gen-label"><Bot class="ai-gen-icon"/> AI generated</p>
            </div>
        </div>

        <pre>{{ commentData }}</pre>

        <AlexiconComponent :type="'markdown'" :val="commentDataData.content"/>

        <!--media-->
        <AlexiconComponent :type="'masonry'" :media="filteredMedia.multimedia" :colsNum="4" v-if="filteredMedia.multimedia.length > 0" :key="keyUpdater"/>
            
        <!-- votes -->
        <div class="CommentRenderer-votes" :key="keyUpdater"><!--up, down, heart, share, options-->
            <div @click="vote('up')">
                <div><ArrowBigUp :color="commentDataData.list_vote_up.includes(AlexiconUserData?.userData?.id) ? '#2ecc71' : ''"/></div>
                <p>{{ commentDataData?.list_vote_up.length }}</p>
            </div>
            <div @click="vote('down')">
                <div><ArrowBigDown :color="commentDataData.list_vote_down.includes(AlexiconUserData?.userData?.id) ? '#cb4335' : ''"/></div>
                <p>{{ commentDataData?.list_vote_down.length }}</p>
            </div>
            <div @click="vote('heart')">
                <div class="vote-heart"><Heart :color="commentDataData.list_vote_heart.includes(AlexiconUserData?.userData?.id) ? '#ff0000' : ''"/></div>
                <p>{{ commentDataData?.list_vote_heart.length }}</p>
            </div>
            <div @click="statisticsActive = true">
                <div><UserSearch/></div>
            </div>
            <div @click="optionsActive = true">
                <div><Ellipsis/></div>
            </div>
        </div>

    </div>

    <!-- statistics n options -->
    <Teleport to="body">
        <StatisticsViewer v-if="statisticsActive" :entityData="commentData" @close="statisticsActive = false"/>
        <OptionsViewer v-if="optionsActive" :entityData="commentData" @close="optionsActive = false"/>
    </Teleport>

</template>

<script>
import { ArrowBigUp, ArrowBigDown, Heart, UserSearch, Ellipsis, Bot } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import StatisticsViewer from './StatisticsViewer.vue';
import OptionsViewer from './OptionsViewer.vue';
import AOS from 'aos'
import 'aos/dist/aos.css'
import ImageProtected from './ImageProtected.vue';

export default {
    name: 'CommentRenderer',
    components: {
        AlexiconComponent, StatisticsViewer, OptionsViewer, ArrowBigUp, ArrowBigDown, Heart, UserSearch, Ellipsis, Bot, ImageProtected
    },
    props: {
        commentData: Object
    },
    data(){
        return{
            AlexiconUserData: {},
            commentDataData: {},
            filteredMedia: {
                multimedia: [],
                files: []
            },
            statisticsActive: false,
            optionsActive: false,
            keyUpdater: 0,
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
            const raw = this.commentDataData?.media;
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

        async vote(voteType){
            const targetId = this.commentDataData.id;
            const entityType = 'comment';

            const result = await this.yipnet_VOTE(this.$ENDPOINT, this.TOKEN(), { voteType, targetId, entityType });
            if(result.response != "Vote updated"){ return; }
            if(result.status == "added"){
                if(!this.commentDataData[`list_vote_${voteType}`].includes(this.AlexiconUserData.userData.id))
                    this.commentDataData[`list_vote_${voteType}`].push(this.AlexiconUserData.userData.id);
            }else
            if(result.status == "removed"){
                const index = this.commentDataData[`list_vote_${voteType}`].indexOf(this.AlexiconUserData.userData.id);
                if(index !== -1)
                    this.commentDataData[`list_vote_${voteType}`].splice(index, 1);
            }
            this.keyUpdater++;
        },
    },
    beforeMount(){
        this.commentDataData = this.commentData;
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.filterMedia();
        AOS.init();
    },
    beforeUnmount() {
        // liberar blobs al salir
        this.cleanupFilteredMediaBlobs();
    },
    watch: {
        postData: {
            deep: true,
            handler(val){
                this.commentDataData = val || {};
                this.filterMedia();
            }
        }
    }
}
</script>

<style scoped>
.CommentRenderer-MAIN{
    width: 100%;
    color: light-dark(black, white);
    margin-bottom: 5px;
    background-color: light-dark(rgba(128,128,128,0.1), rgba(0,0,0,0.15));
    border-radius: 10px;
    padding: 10px;
}

/* head */
.CommentRenderer-head{
    display: flex;
    align-items: center;
    height: fit-content;
}

.CommentRenderer-head > a{
    display: flex;
    width: 50px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    overflow: hidden;
    scale: 0.8;
}

.CommentRenderer-head > a > img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.CommentRenderer-head > div{
    margin-left: 0.4ch;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.CommentRenderer-head > div > p{
    margin: 0;
}

.CommentRenderer-head > div > p:first-child{
    margin-bottom: 0.3ch;
    font-size: 1.6ch;
}

.CommentRenderer-head > div > p:first-child a{
    color: light-dark(black, white);
}

.CommentRenderer-head > div > p:nth-child(2){
    color: gray;
    font-size: 1.4ch;
}

.CommentRenderer-head > div > p:nth-child(2) a{
    color: gray;
}

.CommentRenderer-head > div > p a{
    text-decoration: none;
}

.CommentRenderer-head > div > p a:hover{
    text-decoration: underline;
    cursor: pointer;
}

.ai-gen-label{
    color: gray;
    font-size: 1.4ch;
    margin-top: 0ch !important;
    display: flex;
    align-items: center;
}

.ai-gen-icon{
    margin-right: 0.5ch;
    margin-top: -0.5ch;
    scale: 0.9;
}

/* votes */
.CommentRenderer-votes{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.CommentRenderer-votes > div{
    display: flex;
    align-items: center;
    justify-content: center;
    width: fit-content;
}

.CommentRenderer-votes > div:hover{
    cursor: pointer;
    scale: 1.1;
}

.CommentRenderer-votes > div > div{
    margin-bottom: -5px;
}

.CommentRenderer-votes > div p{
    margin: 0;
    margin-left: 5px;
}

.CommentRenderer-votes .vote-heart > *{
    scale: 0.75;
}
</style>