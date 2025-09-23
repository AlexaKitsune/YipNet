<template>
    <main class="ChatWindow-MAIN">

        <section class="ChatWindow-cover">
            <a :href="getFrontURL()+'/profile/'+userData.id">
                <ImageProtected :mediaId="userData?.current_profile_pic"/>
                <div>
                    <h2>{{ userData.name }} {{ userData.surname }}</h2>
                    <p>{{ parseAndGetLength(userData?.list_positive_external) }} followers</p>
                </div>
            </a>
            <div><!-- search tools --></div>
        </section>

        <section class="ChatWindow-content" ref="ChatWindowContent">
            <MessageRenderer v-for="(item, index) in messages" :key="index" :currentUserId="AlexiconUserData?.userData?.id" :messageData="item"/>
        </section>

        <section class="ChatWindow-buttons">
            <div class="ChatWindow-buttons-preview">
                <div>
                    <div v-for="(item, index) in filesInput.files" :key="index">
                        <img v-if="item.type.includes('image/')" :src="item.url">
                        <video v-if="item.type.includes('video/')">
                            <source :src="item.url+'#t=1'" :type="item.type">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                </div>
                <div>
                    <div v-for="(item, index) in filesInput.files" :key="index">
                        <div v-if="!item.type.includes('image/') && !item.type.includes('video/')">
                            <File/>&nbsp;{{ item.name }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="lucide-icon"><Paperclip/><input type="file" multiple @change="setFilesPreview()" ref="chat-files-input" :disabled="uploading"></div>
            <div class="lucide-icon" @click="deleteFiles()"><Trash2/></div>
            <div class="ChatWindow-buttons-textarea">
                <AlexiconComponent :type="'textarea'" @get-val="(val) => msgText = val" :resize="true" :placeholder="'Comment...'" :disabled="uploading" :key="keyUpdater"/>
            </div>
            <button class="highlighted-btn" @click="sendMessage()" :disabled="msgText?.trim() == ''"><Send style="margin-bottom: -6px;"/></button>
        </section>

    </main>
</template>

<script>
import { Send, Trash2, Paperclip, } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import { io } from 'socket.io-client';
import MessageRenderer from '../comp/MessageRenderer.vue';
import ImageProtected from '../comp/ImageProtected.vue';

export default {
    name: 'ChatWindow',
    components: {
        Send, Paperclip, Trash2, AlexiconComponent, MessageRenderer, ImageProtected,
    },
    data(){
        return{
            AlexiconUserData: {},
            profileId: window.location.href.split("/").pop(),
            userData: {},
            socket: null,
            filesInput: {
                files: []
            },
            uploading: false,
            msgText: '',
            uploadedFilesArray: [],
            keyUpdater: 0,
            messages: [],
        }
    },
    methods: {
        getFrontURL(){
			return window.location.origin;
		},

        parseAndGetLength(str_){
            try {
                return JSON.parse(str_ || '{}').length;
            } catch (error) {
                return 0;
            }
        },

        setFilesPreview() {
            const input = this.$refs["chat-files-input"];
            const files = input.files;

            for (let file of files) {
                const fileType = file.type;

                const isMedia = fileType.startsWith("image/") || fileType.startsWith("video/");

                this.filesInput.files.push({
                    file: file,
                    url: isMedia ? URL.createObjectURL(file) : null,
                    type: fileType,
                    isMedia: isMedia,
                    name: file.name
                });

                if(this.filesInput.files.length >= 50){
                    return;
                }
            }
        },

        deleteFiles(){
            if(this.uploading) return;
            const input = this.$refs["chat-files-input"];
            if (input) {
                input.value = "";
                this.filesInput.files = [];
            }
        },

        async sendMessage(){
            this.uploading = true;
            const files = this.filesInput.files.map(i => i.file);

            if (!files.length) { await this.finallySendMessage(); return; }

            const targetPath = `yipnet/${this.AlexiconUserData.userData.id}/`;
            const visibility = this.privatePost ? 'private' : 'public';
            const CONCURRENCY = 3; // sube de a 3 en paralelo

            const chunks = [];
            for (let i = 0; i < files.length; i += CONCURRENCY) { chunks.push(files.slice(i, i + CONCURRENCY)); }

            try {
                const results = [];
                for (const chunk of chunks) {
                    const partial = await Promise.all(
                        chunk.map(file => this.alexicon_UPLOAD(this.$ENDPOINT, this.TOKEN(), { file, targetPath, visibility }))
                    );
                    results.push(...partial);
                }

                for (const r of results) {
                    if (r?.fileId) this.uploadedFilesArray.push(r.fileId);
                    else if (Array.isArray(r?.mediaIds)) this.uploadedFilesArray.push(...r.mediaIds);
                    else if (Array.isArray(r?.files)) this.uploadedFilesArray.push(...r.files.map(x => x.fileId));
                }

                await this.finallySendMessage();
            } catch (e) {
                console.error("Error al subir los archivos", e);
            } finally {
                this.uploading = false;
            }
        },

        async finallySendMessage(){
            const data = {
                media: this.uploadedFilesArray,
                content: this.msgText,
                targetId: this.userData.id,
                conversationId: 0,
            }

            const result = await this.yipnet_MESSAGE(this.$ENDPOINT, this.TOKEN(), data);

            console.log("Mensaje enviado:", result);
            this.uploading = false;
            this.filesInput.files = [];
            this.msgText = '';
            this.uploadedFilesArray = [];
            this.keyUpdater++;

            this.getMessages();
        },

        async getMessages(){
            //this.messages = [];
            const result = await this.yipnet_GET_MESSAGES(this.$ENDPOINT, this.TOKEN(), this.profileId);
            if(result.status == "ok"){
                console.log("Mensajes recibidos:", result.messages, result.messages[result.messages.length-1].sender_id);
                if(this.messages.length < 1){
                    this.messages = result.messages;
                }else{
                    this.messages.push(result.messages[result.messages.length-1])
                }
            }
            console.log("this.messages", this.messages)
            setTimeout(() => {
                this.$refs.ChatWindowContent.scrollTop = this.$refs.ChatWindowContent.scrollHeight;
            }, 500);
        },

        checkIfMessages() {
            if (this.socket) return; // Evitar crear más de una conexión

            this.socket = io(this.$ENDPOINT);
            this.socket.emit('join', this.AlexiconUserData.userData.id);

            this.socket.on('yipnet_message', (val) => { this.getMessages(val) });
        },
    },
    async mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));

        const result = await this.alexicon_RETRIEVE(this.$ENDPOINT, this.profileId);
        this.userData = result;

        this.getMessages();
        this.checkIfMessages();
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.off('yipnet_message'); // Remover listener
            this.socket.disconnect();            // Cerrar conexión
            this.socket = null;
        }
    }
}
</script>

<style scoped>
.ChatWindow-MAIN {
    height: calc(100vh - 40px);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.ChatWindow-MAIN > section{
    display: inherit;
}

/* cover */
.ChatWindow-cover{
    flex-direction: column;
    background-color: light-dark(#f2f2f2, #2d2d2d);
    box-shadow: 0 0 2ch rgba(0, 0, 0, 0.2);
    border-radius: 0 0 10px 10px;
}

.ChatWindow-cover > a{
    display: flex;
    align-items: center;
    margin-left: 20px;
    text-decoration: none;
    color: unset;
}

.ChatWindow-cover > a img{
    width: 60px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    object-fit: cover;
    object-position: center;
    margin-right: 20px;
}

.ChatWindow-cover > a h2{
    margin-bottom: 0;
}

.ChatWindow-cover > a p{
    margin-top: 0;
    opacity: 0.5;
}

/* content */
.ChatWindow-content{
    height: auto;
    height: 100%;
    max-height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

/* buttons */
.ChatWindow-buttons{
    display: flex;
    align-items: flex-end;
    background-color: light-dark(#f2f2f2, #2d2d2d);
    box-shadow: 0 0 2ch rgba(0, 0, 0, 0.2);
    border-radius: 10px 10px 0 0;
    position: relative;
    padding-top: 5px;
}

/* preview files */
.ChatWindow-buttons-preview{
    background-color: rgba(0, 0, 0, 0.5);
    position: absolute;
    width: calc(100% - 10px);
    bottom: calc(100% + 5px);
    border-radius: 10px;
}

.ChatWindow-buttons-preview{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    max-width: 100%;
    margin-top: 1ch;
}

.ChatWindow-buttons-preview > div{
    width: fit-content;
    max-width: 100%;
    display: flex;
    align-items: center;
    overflow-x: auto;
}

.ChatWindow-buttons-preview > div img, .ChatWindow-buttons-preview > div video{
    max-width: 100px;
    max-height: 100px;
    border-radius: 5px;
    background-color: rgba(128, 128, 128, 0.25);
    margin: 0 5px;
    scale: 0.9;
}

.ChatWindow-buttons-preview > div:last-child{
    width: fit-content;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    max-height: 50vh;
    overflow-y: auto;
}

.ChatWindow-buttons-preview > div:last-child > div{
    width: 100%;
}

.ChatWindow-buttons-preview > div:last-child > div > div{
    display: flex;
}
/* end preview files */ 

.ChatWindow-buttons .lucide-icon{
    margin: 1ch 1.5ch;
}

.PostCreator-buttons button{
    margin-left: auto;
    cursor: pointer;
}

.ChatWindow-buttons .lucide-icon{
    position: relative;
    cursor: pointer;
}

.ChatWindow-buttons .lucide-icon input{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.ChatWindow-buttons-textarea{
    width: 100%;
    margin-right: 1.5ch;
    margin-bottom: 5px;    
}

.ChatWindow-buttons-textarea:deep(.AlexiconTextarea-MAIN){
    display: flex;
    flex-direction: column-reverse;
}

.ChatWindow-buttons-textarea:deep(textarea){
    max-height: 15ch;
    height: 5ch;
    transition: all 0.2s !important;
}

.ChatWindow-buttons-textarea:deep(textarea:focus){
    height: 15ch;
    transition: all 0.2s !important;
}

.ChatWindow-buttons-textarea:deep(.AlexiconMarkdown-MAIN){
    max-height: 15ch;
    height: fit-content;
    min-height: 5ch;
    overflow-y: auto;
}

.ChatWindow-buttons > button{
    margin-right: 1.5ch;
    margin-bottom: calc(1ch + 3px);
}
</style>