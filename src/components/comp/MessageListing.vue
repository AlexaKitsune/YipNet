<template>
    <aside class="MessageListing-MAIN">

        <div v-for="(item, index) in list" :key="index" >

            <!-- direct message -->
            <a v-if="item?.message?.conversation_id == 0" :href="getFrontURL() + '/chat/' + solveDirectionId(item?.message?.sender_id, item?.message?.receiver_id)">
                <ImageProtected :mediaId="item?.other_user?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>{{ item?.other_user?.name }}</p>
                    <p>{{ item?.message?.content }}</p>
                </div>
            </a>

            <!-- group message -->

        </div>

    </aside>
</template>

<script>
import ImageProtected from './ImageProtected.vue';
import { io } from 'socket.io-client';

export default {
    name: 'MessageListing',
    components: {
        ImageProtected,
    },
    data(){
        return{
            myId: JSON.parse(localStorage.getItem("AlexiconUserData")).userData.id,
            list: [],
            socket: null,
        }
    },
    methods: {
        getFrontURL(){
			return window.location.origin;
		},

        solveDirectionId(sender_, receiver_){
            if(sender_ == receiver_) return sender_ || receiver_;
            if(sender_ == this.myId) return receiver_;
            if(receiver_ == this.myId) return sender_;
        },

        async getMessagesList(){
            const result = await window.yipnet.LIST_MESSAGES(this.$ENDPOINT, window.alexicon.TOKEN());
            this.list = result.data.dm_latest;
        },

        checkIfNotifications() {
            if (this.socket) return; // Evitar crear más de una conexión

            this.socket = io(this.$ENDPOINT);
            this.socket.emit('join', this.myId);

            this.socket.on('message', (data) => {
                if(data.content.entityType == "message") this.getMessagesList();
            });
        },
    },
    mounted(){
        this.getMessagesList();    
        this.checkIfNotifications();
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.off('message');
            this.socket.disconnect();            // Cerrar conexión
            this.socket = null;
        }
    }
}
</script>

<style scoped>

.MessageListing-MAIN{
    height: fit-content;
    max-height: 100%;
    overflow: auto;
    padding: 5px;
}

.MessageListing-MAIN > div{
    background-color: light-dark(#f2f2f2, #2d2d2d);
    border-radius: 5px;
    overflow: hidden;
    margin: 0 auto;
    margin-bottom: 10px;
}

.MessageListing-MAIN > div:hover{
    background-color: light-dark(rgba(256,256,256,0.25), rgba(0,0,0,0.15));
}

.MessageListing-MAIN > div a{
    width: 100%;
    text-wrap: nowrap;
    text-overflow: ellipsis;
    height: fit-content;
    display: flex;
    align-items: center;
    color: unset;
    text-decoration: none;
}

.MessageListing-MAIN > div a > img{
    width: 30px;
    aspect-ratio: 1/1;
    object-fit: cover;
    object-position: center;
    border-radius: 100vw;
    margin-left: 5px;
    margin-right: 10px;
}

.MessageListing-MAIN > div a > div {
  min-width: 0;
  flex: 1;
}

.MessageListing-MAIN > div a > div > p {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.MessageListing-MAIN > div a > div > p:first-child{
    margin-top: 0;
    margin-bottom: 0;
}

.MessageListing-MAIN > div a > div > p:last-child{
    margin-top: 0;
    margin-bottom: 0;
    font-size: 1.25ch;
}
</style>