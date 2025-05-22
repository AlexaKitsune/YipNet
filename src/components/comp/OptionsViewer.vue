<template>
    <AlexiconComponent :type="'emergent'" @close="close()" :title="title">

        <section class="OptionsViewer-content">
            <div class="OptionsViewer-options" v-if="mode == ''">
                <div @click="setMode('report')">Report</div>
                <div @click="setMode('delete')">Delete</div>
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
                    <button class="highlighted-btn" @click="perform()">Ok</button>
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

        perform(){
            const id = this.entityData.id;
            const type = this.entityType;
            const mode = this.mode;
            const token = this.AlexiconUserData.token;

            if(mode == 'delete'){            
                fetch(this.$ENDPOINT + "/yipnet/delete", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        id,
                        type,
                    })
                })
                .then(res => res.json())
                .then(data => {
                    console.log("Resultado de eliminación:", data);
                    if (data.status === 'ok') {
                        this.$nextTick(() => {
                            try {
                                const elem = `${type.charAt(0).toUpperCase() + type.slice(1)}Renderer-${id}`;
                                document.getElementById(elem).remove();
                            } catch (error) {
                                console.log("Error updating UI after delete");
                            }
                        });
                        this.close();
                    } else {
                        console.warn("Error en la eliminación:", data.message);
                    }
                })
                .catch(err => {
                    console.error("Error al intentar eliminar:", err);
                });
            }else
            if(mode == 'report'){
                fetch(this.$ENDPOINT + "/alexicon/report", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        service: 'yipnet',
                        type: type,
                        route: (type == 'post' ? '/post/' : '') + id,
                        message: this.reportContent,
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "ok") {
                        console.log("Reporte enviado con éxito");
                        this.close();
                    } else {
                        console.warn("Error al enviar el reporte:", data.message);
                    }
                })
                .catch(err => {
                    console.error("Error de red o servidor:", err);
                });
            }

        }
    },
    beforeMount(){
        this.entityType = this.entityData.comment_date ? 'comment' : 'post';
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