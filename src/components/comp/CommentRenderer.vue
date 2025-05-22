<template>
    <div :class="`CommentRenderer-MAIN CommentRenderer-${commentData.id}`" :id="`CommentRenderer-${commentData.id}`" data-aos="fade-left">

        <div class="CommentRenderer-head">
            <a :href="getFrontURL()+'/profile/'+commentDataData.owner_id"><img :src="commentDataData?.current_profile_pic == '' || typeof commentDataData?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${commentDataData.current_profile_pic}`"></a>
            <div>
                <p><a :href="getFrontURL()+'/profile/'+commentDataData.owner_id">{{ commentDataData.name }} {{commentDataData.surname}}</a></p>
                <p>{{ commentDataData.comment_date }}</p>
            </div>
        </div>

        <AlexiconComponent :type="'markdown'" :val="commentDataData.content"/>

        <!--media-->
        <AlexiconComponent :type="'masonry'" :media="filteredMedia.multimedia" :colsNum="4" v-if="filteredMedia.multimedia.length > 0"/>
            
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
import { ArrowBigUp, ArrowBigDown, Heart, UserSearch, Ellipsis } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import StatisticsViewer from './StatisticsViewer.vue';
import OptionsViewer from './OptionsViewer.vue';
import AOS from 'aos'
import 'aos/dist/aos.css'

export default {
    name: 'CommentRenderer',
    components: {
        AlexiconComponent, StatisticsViewer, OptionsViewer, ArrowBigUp, ArrowBigDown, Heart, UserSearch, Ellipsis,
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
        }
    },
    methods: {
        getFrontURL(){
            return window.location.origin;
        },

        filterMedia(){
            for(let i of this.commentDataData.media){
                if(typeof i != 'string'){ continue; }
                
                const format = i.split(".")[i.split(".").length-1].toLowerCase();
                if(['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'webm'].includes(format)){
                    this.filteredMedia.multimedia.push(this.$ENDPOINT+'/storage/'+i);
                }else{
                    this.filteredMedia.files.push(this.$ENDPOINT+'/storage/'+i);
                }
            }
        },

        vote(voteType){
            const token = this.AlexiconUserData.token;

            const targetId = this.commentDataData.id;
            const entityType = 'comment';

            fetch(this.$ENDPOINT + "/yipnet/vote", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    voteType,
                    targetId,
                    entityType
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Resultado de la votación:", data);
                if(data.response != "Vote updated"){ return; }
                if(data.status == "added"){
                    if(!this.commentDataData[`list_vote_${voteType}`].includes(this.AlexiconUserData.userData.id)){
                        this.commentDataData[`list_vote_${voteType}`].push(this.AlexiconUserData.userData.id);
                    }
                }else
                if(data.status == "removed"){
                    const index = this.commentDataData[`list_vote_${voteType}`].indexOf(this.AlexiconUserData.userData.id);
                    if(index !== -1){
                        this.commentDataData[`list_vote_${voteType}`].splice(index, 1);
                    }
                }
                this.keyUpdater++;
            })
            .catch(err => {
                console.error("Error al enviar la votación:", err);
            });
        },
    },
    beforeMount(){
        this.commentDataData = this.commentData;
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.filterMedia();
        AOS.init();
    }
}
</script>

<style scoped>
.CommentRenderer-MAIN{
    width: 100%;
    color: light-dark(black, white);
    margin-bottom: 5px;
    background-color: light-dark(rgba(128,128,128,0.1), rgba(0,0,0,0.1));
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

.CommentRenderer-head > div > p:last-child{
    color: gray;
    font-size: 1.4ch;
}

.CommentRenderer-head > div > p:last-child a{
    color: gray;
}

.CommentRenderer-head > div > p a{
    text-decoration: none;
}

.CommentRenderer-head > div > p a:hover{
    text-decoration: underline;
    cursor: pointer;
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