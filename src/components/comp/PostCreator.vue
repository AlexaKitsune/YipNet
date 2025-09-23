<template>
    <main class="PostCreator-MAIN">
        
        <section>
            <div class="PostCreator-close" @click="close()"><X/></div>
            <h1>Create post</h1>
            <AlexiconComponent :type="'textarea'" @get-val="(val) => postText = val" :resize="true" :placeholder="'Comment...'" :disabled="uploading"/>
            <div class="PostCreator-images">
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
            <div class="PostCreator-buttons">
                <div class="lucide-icon"><Paperclip/><input type="file" multiple @change="setFilesPreview()" ref="post-files-input" :disabled="uploading"></div>
                <div class="lucide-icon" @click="deleteFiles()"><Trash2/></div>
                <div>
                    <label>
                        <AlexiconComponent :type="'switch'" @get-val="(val) => privatePost = val"/> Private
                    </label>
                    <label>
                        <AlexiconComponent :type="'switch'" @get-val="(val) => nsfwPost = val"/> NSFW
                    </label>
                </div>
                <button :disabled="postText.trim() == '' || uploading" class="highlighted-btn">
                    <LoaderCircle v-if="uploading" class="load-circle"></LoaderCircle>
                    <span v-else @click="post()">Post</span>
                </button>
            </div> 
        </section>

    </main>
</template>

<script>
import { Paperclip, Trash2, X, File, LoaderCircle } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';

export default {
    name: 'PostCreator',
    components: {
        AlexiconComponent, Paperclip, Trash2, X, File, LoaderCircle
    },
    data(){
        return{
            AlexiconUserData: {},
            postText: '',
            filesInput: {
                files: []
            },
            nsfwPost: false,
            privatePost: false,
            uploading: false,
            uploadedFilesArray: [],
        }
    },
    methods: {
        setFilesPreview() {
            const input = this.$refs["post-files-input"];
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
            const input = this.$refs["post-files-input"];
            if (input) {
                input.value = "";
                this.filesInput.files = [];
            }
        },

        post() {
            this.uploading = true;
            const files = this.filesInput.files.map(item => item.file);
            const numFiles = files.length;

            if (numFiles === 0) {
                this.finallyPost();
                return;
            }

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
                    this.finallyPost();
                })
                .catch(err => {
                    console.error("Error al subir uno o más archivos:", err);
                    alert("Error al subir archivos.");
                    this.uploading = false;
                });
        },

        async finallyPost(){
            const newPost = {
                content: this.postText,
                media: JSON.stringify(this.uploadedFilesArray),
                shareId: 0,
                privatePost: this.privatePost,
                nsfwPost: this.nsfwPost
            };
            const result = await this.yipnet_POST(this.$ENDPOINT, this.TOKEN(), newPost);
            console.log("new post created", result)
            this.uploading = false;
            this.$emit('update-post');
            this.$emit('close');
        },

        close(){
            this.editModes = { active: false, type: '' };
            this.$emit('close');
        }
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
    }
}
</script>

<style scoped>
.PostCreator-MAIN{
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

.PostCreator-MAIN > section{
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
    min-width: 50vw;
}

.PostCreator-MAIN > section > h1{
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

/* buttons */
.PostCreator-buttons{
    margin-top: 1ch;
    display: flex;
    align-items: center;
}

.PostCreator-buttons label{
    display: flex;
    align-items: center;
    margin-right: 3ch;
}

.PostCreator-buttons label:deep(label){
    margin-right: 1ch !important;
}

.PostCreator-buttons .lucide-icon{
    margin-right: 3ch;
}

.PostCreator-buttons button{
    margin-left: auto;
}

.PostCreator-buttons .lucide-icon{
    position: relative;
    cursor: pointer;
}

.PostCreator-buttons .lucide-icon input{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.PostCreator-buttons > div > label:nth-child(1){
    margin-bottom: 0.5ch;
}

/* post images and files */
.PostCreator-images{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    max-width: 100%;
    margin-top: 1ch;
}

.PostCreator-images > div{
    width: fit-content;
    max-width: 100%;
    display: flex;
    align-items: center;
    overflow-x: auto;
}

.PostCreator-images > div img, .PostCreator-images > div video{
    max-width: 100px;
    max-height: 100px;
    border-radius: 5px;
    background-color: rgba(128, 128, 128, 0.25);
    margin: 0 5px;
}

.PostCreator-images > div:last-child{
    width: fit-content;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    max-height: 50vh;
    overflow-y: auto;
}

.PostCreator-images > div:last-child > div{
    width: 100%;
}

.PostCreator-images > div:last-child > div > div{
    display: flex;
}

/* load */
.load-circle{
    margin-bottom: -0.5ch;
    animation:spin 1s linear infinite;
}

@keyframes spin { 
    100% { 
        -webkit-transform: rotate(360deg); 
        transform:rotate(360deg); 
    } 
}

.PostCreator-MAIN:deep(textarea){
    max-height: 50vh;
}
</style>