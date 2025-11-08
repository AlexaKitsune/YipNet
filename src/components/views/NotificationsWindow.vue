<template>
    <main class="NotificationsWindow-MAIN">
        
        <h2>Notifications</h2>

        <label>
            <AlexiconComponent :type="'switch'" @get-val="(val) => showHideSeen(val)" :checked="hideSeenNotifications"/>&nbsp; Hide viewed notifications
        </label>

        <div v-for="(item, index) in processedNotifications" :key="index" data-aos="fade-left" @click.stop="markAsSeen(item.id, item.seen)">

            <!-- reaction message -->
            <a v-if="item.content.voteType && item.content.entityType == 'message'" :href="getFrontURL()+'/chat/'+item.content.user.id+'#MessageRenderer'+item.content.targetId" :class="`NotificationsWindow-seen-${item.seen}`">
                <ImageProtected :mediaId="item?.content?.user?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>{{ item.content.user.name }} reacted '{{ item.content.voteType }}' to your message.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- reaction post -->
            <a v-if="item.content.voteType && item.content.entityType != 'message'" :href="getFrontURL()+'/post/'+item.content.targetId" :class="`NotificationsWindow-seen-${item.seen}`">
                <ImageProtected :mediaId="item?.content?.user?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>{{ item.content.user.name }} reacted '{{ item.content.voteType }}' to your post.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- share -->
            <a v-if="item.content.sharedPostId" :href="getFrontURL()+'/post/'+item.content.sharedPostId" :class="`NotificationsWindow-seen-${item.seen}`">
                <ImageProtected :mediaId="item?.content?.user?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>{{ item.content.user.name }} shared your post.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- comment -->
            <a v-if="item.content.commentId" :href="getFrontURL()+'/post/'+item.content.postId+'#CommentRenderer-'+item.content.commentId" :class="`NotificationsWindow-seen-${item.seen}`">
                <ImageProtected :mediaId="item?.content?.user?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>{{ item.content.user.name }} commented on your post.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- follow -->
            <a v-if="item.content.follower_id" :href="getFrontURL()+'/profile/'+item.content.follower_id" :class="`NotificationsWindow-seen-${item.seen}`">
                <ImageProtected :mediaId="item?.content?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>{{ item.content.name }} follows you.</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!-- message -->
            <a v-if="item.content.messageId" :href="getFrontURL()+'/chat/'+item.content.sender_id" :class="`NotificationsWindow-seen-${item.seen}`">
                <ImageProtected :mediaId="item?.content?.user?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                <div>
                    <p>Message from {{ item.content.user.name }}: "{{ item.content.preview }}"</p>
                    <p>{{ item.notif_date }}</p>
                </div>
            </a>

            <!--<pre style="font-size: 1ch;">{{ item }}<hr/></pre>-->

        </div>
        
    </main>
</template>

<script>
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import { io } from 'socket.io-client';
import AOS from 'aos'
import 'aos/dist/aos.css'
import ImageProtected from '../comp/ImageProtected.vue';

export default {
    name: 'NotificantionsWindow',
    components: {
        AlexiconComponent, ImageProtected,
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

            this.socket.on('vote', () => { this.getNotifications(); });
            this.socket.on('follow', () => { this.getNotifications(); });
            this.socket.on('comment', () => { this.getNotifications(); });
        },

        getFrontURL(){
			return window.location.origin;
		},

        async getNotifications(){
            const result = await this.alexicon_NOTIFICATIONS(this.$ENDPOINT, this.TOKEN());
            // Reset antes de llenar
            this.allNotifications = [];
            this.unseenNotifications = 0;

            for(let i of result.notifications){
                if(i.service == 'yipnet' || (i.service == 'alexicon' && i.content.follower_id))
                    this.allNotifications.push(i);
                if(!i.seen)
                    this.unseenNotifications++;
            }

            const r = result.notifications[0];
            if(r?.service == 'yipnet' && r?.content.entityType == 'message') this.$emit('update-chat-window', { userId: r.content.user.id, msgId: r.content.targetId });

            this.processedNotifications = this.allNotifications;
            this.$emit('update-notifications', this.unseenNotifications);
        },

        async markAsSeen(id_, seen_){
            if(seen_ === true) return;
            const result = await this.alexicon_NOTIFICATION_SEEN(this.$ENDPOINT, this.TOKEN(), { id: id_ });
            if(result.status == "ok") this.getNotifications();
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
            this.socket.off('vote'); // Remover listener
            this.socket.off('follow');
            this.socket.off('comment');
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
    width: fit-content;
}

.NotificationsWindow-MAIN > div{
    background-color: light-dark(#f2f2f2, #2d2d2d);
    border-radius: 5px;
    overflow: hidden;
    max-width: 75ch;
    margin: 0 auto;
    margin-bottom: 10px;
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
    object-fit: cover;
    object-position: center;
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