<template>
    <section :class="`MessageRenderer-MAIN side-${ currentUserId == messageData.sender_id ? 'right' : 'left' }`">

        <div class="msg-bubble">
            <AlexiconComponent :type="'markdown'" :val="messageData?.content || ''"/>
            <!-- media -->
            <AlexiconComponent :type="'masonry'" :media="filteredMedia.multimedia" :colsNum="3" v-if="filteredMedia.multimedia.length > 0" :key="keyUpdater"/>
            <div v-for="(item, index) in filteredMedia.files" :key="index" class="PostRenderer-doc">
                <AlexiconComponent :type="'doc'" :val="item" v-if="filteredMedia.files.length > 0" :key="keyUpdater" />
            </div>
        </div>

    </section>
</template>

<script>
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';

export default {
    name: 'MessageRenderer',
    components: {
        AlexiconComponent,
    },
    props: {
        currentUserId: Number,
        messageData: Object,
    },
    data(){
        return{
            AlexiconUserData: {},
            messageDataData: {},
            filteredMedia: {
                multimedia: [],
                files: []
            },
        }
    },
    methods: {
        // Limpia blob URLs de filteredMedia (llámala si reprocesas la lista)
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

    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.messageDataData = this.messageData;
        this.filterMedia();
    },
    beforeUnmount() {
        this.cleanupFilteredMediaBlobs(); // liberar blobs al salir
    },
    watch: {
        messageData: {
            deep: true,
            handler(val){
                this.messageDataData = val || {};
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

.side-right > .msg-bubble{
    background-color: #7701FF;
}

.side-left > .msg-bubble{
    background-color: gray;
}

.PostRenderer-doc{
    margin-top: 5px;
}
</style>