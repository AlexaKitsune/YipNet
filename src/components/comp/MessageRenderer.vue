<template>
    <section :class="`MessageRenderer-MAIN side-${ currentUserId == messageData.sender_id ? 'right' : 'left' }`" :id="`MessageRenderer${messageData.id}`">

        <div class="msg-bubble">
            <div>
                <AlexiconComponent :type="'markdown'" :val="messageData?.content || ''"/>
            </div>
            <!-- media -->
            <AlexiconComponent :type="'masonry'" :media="filteredMedia.multimedia" :colsNum="3" v-if="filteredMedia.multimedia.length > 0" :key="keyUpdater" />
            <div v-for="(item, index) in filteredMedia.files" :key="index" class="MessageRenderer-doc">
                <AlexiconComponent :type="'doc'" :val="item" v-if="filteredMedia.files.length > 0" :key="keyUpdater" />
            </div>
        </div>
        
        <!--votes-->
        <div class="MessageRenderer-votes" :key="keyUpdater"><!--up, down, heart-->
            <div @click="vote('up')">
                <div><ArrowBigUp :color="messageDataData?.list_vote_up?.includes(AlexiconUserData?.userData?.id) ? '#2ecc71' : ''"/></div>
                <p>{{ messageDataData?.list_vote_up?.length }}</p>
            </div>
            <div @click="vote('down')">
                <div><ArrowBigDown :color="messageDataData?.list_vote_down?.includes(AlexiconUserData?.userData?.id) ? '#cb4335' : ''"/></div>
                <p>{{ messageDataData?.list_vote_down?.length }}</p>
            </div>
            <div @click="vote('heart')">
                <div class="vote-heart"><Heart :color="messageDataData?.list_vote_heart?.includes(AlexiconUserData?.userData?.id) ? '#ff0000' : ''"/></div>
                <p>{{ messageDataData?.list_vote_heart?.length }}</p>
            </div>
            <div @click="statisticsActive = true">
                <div style="scale:0.7;"><UserSearch/></div>
            </div>
            <div @click="optionsActive = true">
                <div style="scale:0.9;"><Ellipsis/></div>
            </div>
        </div>

    </section>

    <!-- statistics n options -->
    <StatisticsViewer v-if="statisticsActive" :entityData="messageData" @close="statisticsActive = false"/>
    <OptionsViewer v-if="optionsActive" :entityData="messageData" @close="optionsActive = false"/>

</template>

<script>
import { ArrowBigUp, ArrowBigDown, Heart, UserSearch, Ellipsis } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import StatisticsViewer from './StatisticsViewer.vue';
import OptionsViewer from './OptionsViewer.vue';

export default {
    name: 'MessageRenderer',
    components: {
        AlexiconComponent, ArrowBigUp, ArrowBigDown, Heart, UserSearch, Ellipsis, StatisticsViewer, OptionsViewer
    },
    props: {
        currentUserId: Number,
        messageData: Object,
    },
    data(){
        return{
            AlexiconUserData: JSON.parse(localStorage.getItem("AlexiconUserData")),
            messageDataData: {},
            filteredMedia: {
                multimedia: [],
                files: []
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
            const raw = this.messageDataData?.media;
            if (Array.isArray(raw)) ids = raw;
            else if (typeof raw === 'string' && raw.trim()) {
                try { ids = JSON.parse(raw); } catch { ids = []; }
            }

            // filtrar valores no numéricos / nulos
            ids = ids.filter(id => Number.isFinite(+id));

            if (!ids.length) return;

            // 3) resolver todos con tu helper
            const endpoint = this.$ENDPOINT;
            const token = window.alexicon.TOKEN?.();
            const results = await Promise.all(
                ids.map(id => window.alexicon.MEDIA_FILE(endpoint, token, id).catch(() => null))
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

        async vote(voteType){
            const targetId = this.messageData.id;
            const entityType = "message";
            const result = await window.yipnet.VOTE(this.$ENDPOINT, window.alexicon.TOKEN(), { voteType, targetId, entityType });
            console.log(result)
            this.$parent.updateMessageVoted(targetId);
        },

        parseArrayMaybe(jsonish) {
            if (Array.isArray(jsonish)) return jsonish;
            if (typeof jsonish === 'string') {
                try { const a = JSON.parse(jsonish); return Array.isArray(a) ? a : []; }
                catch { return []; }
            }
            return [];
        },

        normalizeMessage(msg) {
            const base = msg ? JSON.parse(JSON.stringify(msg)) : {}; // clonado para no mutar el prop
            base.list_vote_up    = this.parseArrayMaybe(base.list_vote_up);
            base.list_vote_down  = this.parseArrayMaybe(base.list_vote_down);
            base.list_vote_heart = this.parseArrayMaybe(base.list_vote_heart);
            base.media           = this.parseArrayMaybe(base.media);
            return base;
        },

    },
    mounted(){
        this.messageDataData = this.normalizeMessage(this.messageData);
        this.filterMedia();
    },
    beforeUnmount() {
        this.cleanupFilteredMediaBlobs(); // liberar blobs al salir
    },
    watch: {
        messageData: {
            immediate: false, // ya hicimos el mounted
            deep: false,      // con reemplazo de objeto basta; si necesitas detectar cambios internos, pon true
            handler(newVal) {
                this.messageDataData = this.normalizeMessage(newVal);
                this.filterMedia();
            }
        }
    }
}
</script>

<style scoped>
.MessageRenderer-MAIN{
    width: calc(100% - 20px - 5px);
    padding: 10px;
    display: flex;
    flex-direction: column;
}

.side-left{
    align-items: flex-start;
}

.side-right{
    align-items: flex-end;
}

.msg-bubble{
    width: fit-content;
    max-width: 75%;
    padding: 10px;
    color: white;
    border-radius: 10px;
}

.msg-bubble:deep(.AlexiconMasonry-MAIN){
    margin-top: 5px !important;
}

.msg-bubble:deep(.AlexiconDoc-MAIN){
    margin-top: 10px !important;
}

.msg-bubble > div:first-child:deep(p:first-child),
.msg-bubble > div:first-child:deep(h1:first-child),
.msg-bubble > div:first-child:deep(h2:first-child),
.msg-bubble > div:first-child:deep(h3:first-child),
.msg-bubble > div:first-child:deep(h4:first-child),
.msg-bubble > div:first-child:deep(h5:first-child),
.msg-bubble > div:first-child:deep(h6:first-child){
    margin-top: 0;
}

.msg-bubble > div:first-child:deep(p:last-child),
.msg-bubble > div:first-child:deep(h1:last-child),
.msg-bubble > div:first-child:deep(h2:last-child),
.msg-bubble > div:first-child:deep(h3:last-child),
.msg-bubble > div:first-child:deep(h4:last-child),
.msg-bubble > div:first-child:deep(h5:last-child),
.msg-bubble > div:first-child:deep(h6:last-child){
    margin-bottom: 0;
}

.side-right > .msg-bubble{
    background-color: #7701FF;
}

.side-left > .msg-bubble{
    background-color: light-dark(rgb(219, 219, 219), rgb(80, 80, 80));
    color: light-dark(black, white);
}

.MessageRenderer-doc{
    margin-top: 5px;
}

/* votes */
.MessageRenderer-votes{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 0;
    scale: 0.8;
    padding-bottom: 0;
    margin: 0 -15px;
}

.MessageRenderer-votes > div{
    display: flex;
    align-items: center;
    justify-content: center;
    width: fit-content;
}

.side-right .MessageRenderer-votes > div{
    margin-left: 20px;
}

.side-left .MessageRenderer-votes > div{
    margin-right: 20px;
}

.MessageRenderer-votes > div:hover{
    cursor: pointer;
    scale: 1.1;
}

.MessageRenderer-votes > div > div{
    margin-bottom: -5px;
}

.MessageRenderer-votes > div p{
    margin: 0;
    margin-left: 5px;
}

.MessageRenderer-votes .vote-heart > *{
    scale: 0.75;
}
</style>