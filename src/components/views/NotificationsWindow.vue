<template>
    <main class="NotificationsWindow-MAIN">
        
        <h2>Notifications</h2>

        <label>
            <AlexiconComponent :type="'switch'" @get-val="(val) => showHideSeen(val)" :checked="hideSeenNotifications"/>&nbsp; Hide viewed notifications
        </label>

        <div v-for="(item, index) in processedNotifications" :key="index" data-aos="fade-left" @click.stop="markAsSeen(item.id, item.seen)">

            <!-- reaction -->
            <a v-if="item.content.voteType" :href="getFrontURL()+'/post/'+item.content.targetId" :class="`NotificationsWindow-seen-${item.seen}`">
                <img :src="item.content.user.current_profile_pic == '' || typeof item.content.user.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.content.user.current_profile_pic}`">
                <div>
                    <p>{{ item.content.user.name }} reacted '{{ item.content.voteType }}' to your post.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- share -->
            <a v-if="item.content.sharedPostId" :href="getFrontURL()+'/post/'+item.content.sharedPostId" :class="`NotificationsWindow-seen-${item.seen}`">
                <img :src="item.content.user.current_profile_pic == '' || typeof item.content.user.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.content.user.current_profile_pic}`">
                <div>
                    <p>{{ item.content.user.name }} shared your post.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- comment -->
            <a v-if="item.content.commentId" :href="getFrontURL()+'/post/'+item.content.postId+'#CommentRenderer-'+item.content.commentId" :class="`NotificationsWindow-seen-${item.seen}`">
                <img :src="item.content.user.current_profile_pic == '' || typeof item.content.user.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.content.user.current_profile_pic}`">
                <div>
                    <p>{{ item.content.user.name }} commented on your post.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- follow -->
            <a v-if="item.content.follower_id" :href="getFrontURL()+'/profile/'+item.content.follower_id" :class="`NotificationsWindow-seen-${item.seen}`">
                <img :src="item.content.current_profile_pic == '' || typeof item.content.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.content.current_profile_pic}`">
                <div>
                    <p>{{ item.content.name }} follows you.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

        </div>
        
    </main>
</template>

<script>
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import { io } from 'socket.io-client';
import AOS from 'aos'
import 'aos/dist/aos.css'

export default {
    name: 'NotificantionsWindow',
    components: {
        AlexiconComponent,
    },
    data(){
        return{
            AlexiconUserData: {},
            allNotifications: [],
            processedNotifications: [],
            socket: null,
            unseenNotifications: 0,
            hideSeenNotifications: false,
        }
    },
    methods: {
        checkIfNotifications() {
            if (this.socket) return; // Evitar crear más de una conexión

            this.socket = io(this.$ENDPOINT);
            this.socket.emit('join', this.AlexiconUserData.userData.id);

            this.socket.on('yipnet_notification', () => { this.getNotifications(); });
            this.socket.on('follow_notification', () => { this.getNotifications(); });
        },

        getFrontURL(){
			return window.location.origin;
		},

        getNotifications(){
            const token = this.AlexiconUserData.token;
            this.processedNotifications = [];
            this.unseenNotifications = 0;

            fetch(this.$ENDPOINT + "/alexicon/notifications", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                for(let i of data.notifications){
                    if(i.service == 'yipnet' || (i.service == 'alexicon' && i.content.follower_id)){
                        this.allNotifications.push(i);
                    }
                    if(!i.seen){
                        this.unseenNotifications++;
                    }
                }
                this.processedNotifications = this.allNotifications;
                this.$emit('update-notifications', this.unseenNotifications);
            })
            .catch(err => {
                console.error("Error de red o servidor:", err);
            });
        },

        markAsSeen(id_, seen_){
            if(seen_ === true) return;
            const token = this.AlexiconUserData.token;

            fetch(this.$ENDPOINT + "/alexicon/notification_seen", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    id: id_
                })
            })
            .then(res => res.json())
            .then(data => {
                if(data.status == "ok"){
                    this.getNotifications();
                }
            })
            .catch(err => {
                console.error("Error de red o servidor:", err);
            });
        },

        showHideSeen(mode_){
            const hidden = this.hideSeenNotifications;
            if(mode_ == hidden) return;
            this.hideSeenNotifications = mode_;

            if(mode_){
                this.processedNotifications = [];
                for(let i of this.allNotifications){
                    if(!i.seen){
                        this.processedNotifications.push(i);
                    }
                }
            }else{
                this.processedNotifications = this.allNotifications;
            }
        }
    },
    mounted(){
        console.log('mounted')
		this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.checkIfNotifications();
        this.getNotifications();
        AOS.init();
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.off('vote_notification'); // Remover listener
            this.socket.disconnect();            // Cerrar conexión
            this.socket = null;
        }
    }
}
</script>

<style scoped>
label{
    display: flex;
    align-items: center;
    margin-bottom: 30px;
}

.NotificationsWindow-MAIN > div{
    margin-bottom: 10px;
    background-color: light-dark(#f2f2f2, #2d2d2d);
    border-radius: 5px;
    overflow: hidden;
}

.NotificationsWindow-MAIN > div:hover{
    background-color: light-dark(rgba(256,256,256,0.25), rgba(0,0,0,0.15));
}

.NotificationsWindow-MAIN > div a{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    color: unset;
    text-decoration: none;
}

.NotificationsWindow-MAIN > div a > img{
    width: 50px;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    margin-left: 10px;
    margin-right: 15px;
}

.NotificationsWindow-MAIN > div a > div > p:first-child{
    margin-bottom: 0;
}

.NotificationsWindow-MAIN > div a > div > p:last-child{
    margin-top: 0;
    font-size: 1.25ch;
    opacity: 0.5;
}

.NotificationsWindow-seen-false{
    border-left: 10px solid #7701ff;
 }

.NotificationsWindow-seen-true{
    border-left: 10px solid light-dark(rgba(128, 128, 128, 0.5), rgba(128, 128, 128, 0.25));
}
</style>