<template>
    <main class="AlexiconMasonry-MAIN">
        <div
            class="AlexiconMasonry-col"
            :style="`width: ${100 / realColsNum}%;`"
            v-for="(item, index) in finalArray"
            :key="index"
        >
            <div v-for="subItem in item" :key="subItem.id">
                <a
                    v-if="isImage(subItem)"
                    :href="subItem.fullUrl"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <img :src="subItem.fullUrl">
                </a>

                <a
                    v-else-if="isVideo(subItem)"
                    :href="subItem.fullUrl"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <video controls>
                        <source :src="subItem.fullUrl" :type="subItem.type">
                    </video>
                </a>
            </div>
        </div>
    </main>
</template>

<script>
export default {
    name: 'AlexiconMasonry',

    props: {
        media: {
            type: Array,
            default: () => []
        },

        colsNum: {
            type: Number,
            default: 3
        }
    },

    computed: {
        realColsNum() {
            return Math.max(
                1,
                Math.min(this.media.length, this.colsNum)
            )
        },

        finalArray() {
            const result = []

            for (let i = 0; i < this.realColsNum; i++) {
                result.push([])
            }

            this.media.forEach((item, index) => {
                result[index % this.realColsNum].push(item)
            })

            return result
        }
    },

    methods: {
        isImage(item) {
            return item.type?.startsWith('image/')
        },

        isVideo(item) {
            return item.type?.startsWith('video/')
        }
    }
}
</script>

<style scoped>
.AlexiconMasonry-MAIN {
    width: 100%;
    display: flex;
    margin-top: 1rem;
}

.AlexiconMasonry-col {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.AlexiconMasonry-col > div {
    width: 100%;
    display: block;
}

.AlexiconMasonry-col > div > a {
    display: block;
    width: 100%;
}

.AlexiconMasonry-col > div > a > img,
.AlexiconMasonry-col > div > a > video {
    display: block;
    width: 100%;
    border-radius: 5px;
    scale: 0.97;
    margin: 0;
    background-color: rgba(0, 0, 0, 0.75);
}

.AlexiconMasonry-col > div > a > img:hover,
.AlexiconMasonry-col > div > a > video:hover {
    cursor: pointer;
    filter: brightness(0.8);
    transition: filter 0.2s;
}
</style>