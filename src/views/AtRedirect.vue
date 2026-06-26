<template>
    <YipNetLayout :user-data="userData" :on-session="onSession">
        <div class="p-6 text-center opacity-70">
            Redirecting...
        </div>
    </YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import { getUserByAt } from '@/services/alexicon/users'

export default {
    name: 'AtRedirect',

    components: {
        YipNetLayout
    },

    props: {
        userData: {
            type: Object,
            default: () => ({})
        },
        onSession: {
            type: Boolean,
            default: false
        }
    },

    async mounted() {
        try {
            const result = await getUserByAt(this.$route.params.at)
            const id = result.data?.id

            if (id) {
                this.$router.replace(`/user/${id}`)
            } else {
                this.$router.replace('/not-found')
            }
        } catch {
            this.$router.replace('/not-found')
        }
    }
}
</script>