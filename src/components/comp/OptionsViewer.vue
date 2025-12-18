<template>
    <AlexiconComponent :type="'emergent'" @close="close()" :title="title">

        <section class="OptionsViewer-content">
            <div class="OptionsViewer-options" v-if="mode == ''">
                <div @click="setMode('report')" v-if="AlexiconUserData?.userData?.id != (entityData?.owner_id ?? entityData.sender_id)">Report</div>
                <div @click="setMode('delete')" v-if="AlexiconUserData?.userData?.id == (entityData?.owner_id ?? entityData.sender_id)">Delete</div>
            </div>
            <div class="OptionsViewer-inside" v-else>
                <MoveLeft @click="setMode('')" style="cursor: pointer;"/>

                <div>
                    <h4>{{ msg.title }}</h4>
                    <p>{{ msg.content }}</p>
                </div>

                <textarea v-if="mode == 'report'" v-model="reportContent" placeholder="Add comment.."></textarea>

                <br>
                <div>
                    <button @click="setMode('')">Cancel</button>
                    <button class="highlighted-btn" @click="perform()" :disabled="mode == 'report' && reportContent.trim() == ''">Ok</button>
                </div>
            </div>
        </section>

    </AlexiconComponent>
</template>

<script>
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import { MoveLeft } from 'lucide-vue-next';

export default {
    name: 'OptionsViewer',
    components: {
        AlexiconComponent, MoveLeft
    },
    props: {
        entityData: Object
    },
    data(){
        return{
            AlexiconUserData: {},
            mode: '',
            title: 'Options',
            msg: {
                title: '',
                content: ''
            },
            entityType: '',
            reportContent: ''
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
            let txt;
            if(mode_ == '') txt = "Options";
            if(mode_ == 'report'){
                txt = "Report";
                this.msg.title = `Report ${this.entityType}?`;
                this.msg.content = `This ${this.entityType} will be under review.`;
            }
            if(mode_ == 'delete'){
                txt = "Delete";
                this.msg.title = `Delete ${this.entityType}?`;
                this.msg.content = `This ${this.entityType} and all associated data (reactions, ${this.entityType == 'post' ? 'shares, comments' : ''}etc) will be deleted.`;
            }
            this.title = txt;
        },

        async perform(){
            const id = this.entityData.id;
            const type = this.entityType;
            const mode = this.mode;

            if(mode == 'delete'){
                const result = await window.yipnet.DELETE(this.$ENDPOINT, window.alexicon.TOKEN(), {id, type });
                if (result.status === 'ok') {
                    this.$nextTick(() => {
                        try {
                            const elem = `${type.charAt(0).toUpperCase() + type.slice(1)}Renderer-${id}`;
                            document.getElementById(elem).remove();
                        } catch (error) {
                            console.log(this.entityType != 'message' ? "Error updating UI after delete" : "closing on msg");
                        }
                    });
                    this.close();
                }
            }else
            if(mode == 'report'){
                const reportData = {
                    service: 'yipnet',
                    type,
                    route: (type == 'post' ? '/post/' : '') + id,
                    message: this.reportContent,
                };

                const result = await window.alexicon.REPORT(this.$ENDPOINT, window.alexicon.TOKEN(), reportData);
                if (result.status === "ok") {
                    console.log("Reporte enviado con éxito");
                    this.close();
                }
            }
        },
    },
    beforeMount(){
        if(this.entityData.sender_id){
            this.entityType = 'message';
        }else{
            this.entityType = this.entityData.comment_date ? 'comment' : 'post';
        }
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
    }
}
</script>

<style scoped>
.OptionsViewer-content{
    margin-top: 10px;
    overflow-y: auto;
    max-height: 70vh;
}

.OptionsViewer-options > div{
    padding: 10px 10px;
    border-radius: 5px;
}

.OptionsViewer-options > div:hover{
    cursor: pointer;
    background-color: rgba(128, 128, 128, 0.25);
}

.OptionsViewer-inside > div:last-child{
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.OptionsViewer-inside > div:last-child button{
    margin-left: 3ch;
}

textarea{
    width: calc(100% - 2ch);
    resize: vertical;
    margin-bottom: 1ch;
    min-height: 10ch;
    padding: 5px;
}
</style>