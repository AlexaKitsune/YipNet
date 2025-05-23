<template>
    <main class="ChatWindow-MAIN">

        <section class="ChatWindow-cover">
            <a :href="getFrontURL()+'/profile/'+userData.id">
                <img :src="userData?.current_profile_pic == '' || typeof userData?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${userData.current_profile_pic}`">
                <div>
                    <h2>{{ userData.name }} {{ userData.surname }}</h2>
                    <p>{{ parseAndGetLength(userData?.list_positive_external) }} followers</p>
                </div>
            </a>
            <div><!-- search tools --></div>
        </section>

        <section class="ChatWindow-content">
            
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

export default {
    name: 'ChatWindow',
    components: {
        Send, Paperclip, Trash2, AlexiconComponent
    },
    data(){
        return{
            AlexiconUserData: {},
            profileId: 0,
            userData: {},
            filesInput: {
                files: []
            },
            uploading: false,
            msgText: '',
            uploadedFilesArray: [],
            keyUpdater: 0,
        }
    },
    methods: {
        getProfileId(){
			const path = new URL(window.location.href).pathname;
			let pathArray = path.split("/");
			// eslint-disable-next-line
			let x = pathArray.shift();
			this.profileId = pathArray[1];
        },

        getPublicUserData(){
            fetch(`${this.$ENDPOINT}/alexicon/retrieve/?id=${this.profileId}`, {
                method: 'GET'
            })
            .then(res => res.json())
            .then(data => {
                this.userData = data;
            })
        },

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
            if(this.uploading){
                return;
            }
            const input = this.$refs["chat-files-input"];
            if (input) {
                input.value = "";
                this.filesInput.files = [];
            }
        },

        sendMessage(){
            this.uploading = true;
            const files = this.filesInput.files.map(item => item.file);
            const numFiles = files.length;

            if (numFiles === 0) {
                this.finallySendMessage();
                return;
            }

            const token = this.AlexiconUserData.token;
            const targetPath = `yipnet/${this.AlexiconUserData.userData.id}/`;

            const uploadPromises = Array.from(files).map(file => {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('targetPath', targetPath);

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
                        this.uploadedFilesArray.push(i.relativePath);
                    }
                    this.finallyPost();
                })
                .catch(err => {
                    console.error("Error al subir uno o más archivos:", err);
                    alert("Error al subir archivos.");
                    this.uploading = false;
                });
        },

        finallySendMessage(){
            const token = this.AlexiconUserData.token;
            fetch(this.$ENDPOINT+"/yipnet/message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({
                    media: this.uploadedFilesArray,
                    content: this.msgText,
                    targetId: this.userData.id,
                    conversationId: 0,
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Mensaje enviado:", data);
                this.uploading = false;
                this.filesInput.files = [];
                this.msgText = '';
                this.uploadedFilesArray = [];
                this.keyUpdater++;
            })
            .catch(err => {
                console.error("Error al enviar mensaje:", err);
                this.uploading = false;
            });
        },

        checkIfMessages() {
            if (this.socket) return; // Evitar crear más de una conexión

            this.socket = io(this.$ENDPOINT);
            this.socket.emit('join', this.AlexiconUserData.userData.id);

            this.socket.on('yipnet_message', () => { this.getMessages(); });
        },

        getMessages(){
            const token = this.AlexiconUserData.token;
            fetch(this.$ENDPOINT + "/yipnet/get_messages?user=" + this.profileId, {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + token
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "ok") {
                    console.log("Mensajes recibidos:", data.messages);
                    // Aquí puedes asignarlos a una variable de Vue
                    this.messages = data.messages;
                } else {
                    console.error("Error en la respuesta:", data.message);
                }
            })
            .catch(error => {
                console.error("Error en la petición:", error);
            });
        }
        
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.getProfileId();
        this.getPublicUserData();
        
        this.checkIfMessages();
        this.getMessages();
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
    border: 1px solid red;
    height: 100%;
    max-height: 100%;
    overflow-y: auto;
}

/* buttons */
.ChatWindow-buttons{
    display: flex;
    align-items: flex-end;
    background-color: light-dark(#f2f2f2, #2d2d2d);
    box-shadow: 0 0 2ch rgba(0, 0, 0, 0.2);
    border-radius: 10px 10px 0 0;
    position: relative;
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
    margin-bottom: 1ch;    
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