<template>
    <AlexiconComponent :type="'emergent'" @close="close()" :title="title">

        <div class="StatisticsViewer-menu">
            <div :style="`width: ${entityData.comment_date ? 33.3 : 25}%;`" :class="`StatisticsViewer-btn-${mode == 'up'}`" @click="setMode('up')"><ArrowBigUp/></div>
            <div :style="`width: ${entityData.comment_date ? 33.3 : 25}%;`" :class="`StatisticsViewer-btn-${mode == 'down'}`" @click="setMode('down')"><ArrowBigDown/></div>
            <div :style="`width: ${entityData.comment_date ? 33.3 : 25}%;`" :class="`StatisticsViewer-btn-${mode == 'heart'}`" @click="setMode('heart')"><Heart style="scale:0.8;"/></div>
            <div :style="`width: ${entityData.comment_date ? 33.3 : 25}%;`" :class="`StatisticsViewer-btn-${mode == 'share'}`" @click="setMode('share')" v-if="!entityData.comment_date"><Forward/></div>
        </div>
        
        <section class="StatisticsViewer-content">
            <div v-if="mode == 'up'">
                <div class="StatisticsViewer-render-users" v-for="(item, index) in arrays.up" :key="index">
                    <a :href="getFrontURL()+'/profile/'+item.id">
                        <ImageProtected :mediaId="item?.current_profile_pic"/><!--or require('../../assets/pfp.png')-->
                        <p>{{ item.name }} {{ item.surname }}</p>
                    </a>
                </div>
                <p v-if="arrays.up.length == 0">No reactions yet.</p>
            </div>
            <div v-if="mode == 'down'">
                <div class="StatisticsViewer-render-users" v-for="(item, index) in arrays.down" :key="index">
                    <a :href="getFrontURL()+'/profile/'+item.id">
                        <img :src="item?.current_profile_pic == '' || typeof item?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.current_profile_pic}`">
                        <p>{{ item.name }} {{ item.surname }}</p>
                    </a>
                </div>
                <p v-if="arrays.down.length == 0">No reactions yet.</p>
            </div>
            <div v-if="mode == 'heart'">
                <div class="StatisticsViewer-render-users" v-for="(item, index) in arrays.heart" :key="index">
                    <a :href="getFrontURL()+'/profile/'+item.id">
                        <img :src="item?.current_profile_pic == '' || typeof item?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.current_profile_pic}`">
                        <p>{{ item.name }} {{ item.surname }}</p>
                    </a>
                </div>
                <p v-if="arrays.heart.length == 0">No reactions yet.</p>
            </div>
            <div v-if="mode == 'share' && !entityData.comment_date">
                <div class="StatisticsViewer-render-users" v-for="(item, index) in arrays.share" :key="index">
                    <a :href="getFrontURL()+'/post/'+item.id">
                        <img :src="item?.current_profile_pic == '' || typeof item?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item.current_profile_pic}`">
                        <p>{{ item.name }} {{ item.surname }}</p>
                    </a>
                </div>
                <p v-if="arrays.share.length == 0">No shares yet.</p>
            </div>

        </section>

    </AlexiconComponent>
</template>

<script>
import { ArrowBigUp, ArrowBigDown, Heart, Forward } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import ImageProtected from './ImageProtected.vue';

export default{
    name: 'StatisticsViewer',
    components: {
        AlexiconComponent, ArrowBigUp, ArrowBigDown, Heart, Forward, ImageProtected
    },
    props: {
        entityData: Object
    },
    data(){
        return{
            AlexiconUserData: {},
            mode: '',
            title: '0',
            arrays: {
                up: [],
                down: [],
                heart: [],
                share: []
            }
        }
    },
    methods: {
        close(){
            this.$emit('close', true);
        },

        getFrontURL(){
			return window.location.origin;
		},

        setMode(mode_){
            this.mode = mode_;
            const num = this.arrays[mode_].length;
            let txt;
            if(mode_ == 'up') txt = "Up votes";
            if(mode_ == 'down') txt = "Down votes";
            if(mode_ == 'heart') txt = "Heart reactions";
            if(mode_ == 'share') txt = "Shares";
            this.title = `${txt} ${num}`;
        }
    },
    async mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));

        this.arrays['up'] = await this.alexicon_RETRIEVE_USERS(this.$ENDPOINT, { ids: this.entityData.list_vote_up });
        this.arrays['down'] = await this.alexicon_RETRIEVE_USERS(this.$ENDPOINT, { ids: this.entityData.list_vote_down });
        this.arrays['heart'] = await this.alexicon_RETRIEVE_USERS(this.$ENDPOINT, { ids: this.entityData.list_vote_heart });
        this.arrays['share'] = await this.alexicon_RETRIEVE_POSTS(this.$ENDPOINT, { ids: this.entityData.shared_by_list });
        
        this.$nextTick(() => {
            setTimeout(() => {
                this.setMode('up');
            }, 500);
        });
    }
}
</script>

<style scoped>
.StatisticsViewer-menu{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.StatisticsViewer-menu > div{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 5px;
}

.StatisticsViewer-btn-true{
    color: white;
    background-color: #7701ff;
    padding: 5px 0;
}

.StatisticsViewer-content{
    margin-top: 10px;
    overflow-y: auto;
    max-height: 70vh;
}

.StatisticsViewer-render-users, .StatisticsViewer-render-users a{
    display: flex;
    align-items: center;
}

.StatisticsViewer-render-users a{
    cursor: pointer;
    text-decoration: none;
    color: unset;
    width: 100%;
    padding: 3px 5px;
    border-radius: 5px;
}

.StatisticsViewer-render-users a:hover{
    background-color: rgba(128, 128, 128, 0.25);
}

.StatisticsViewer-render-users img{
    width: 50px;
    border-radius: 100vw;
    margin-right: 10px;
    aspect-ratio: 1/1;
    object-fit: cover;
    object-position: center;
}

.StatisticsViewer-content > div > p{
    opacity: 0.5;
    text-align: center;
}
</style>