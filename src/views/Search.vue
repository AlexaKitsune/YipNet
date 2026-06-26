<template>
    <YipNetLayout :user-data="userData" :on-session="onSession" class="Search-MAIN">
        <br/>
        
        <main class="mx-auto max-w-[1080px] space-y-6">
            <h1 class="text-2xl font-bold">{{ $t('search.title') }}</h1>

            <YipNetSearch
                mode="global"
                :initial-q="$route.query.q || ''"
            />
        </main>
    </YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import YipNetSearch from '@/components/YipNetSearch.vue'

export default {
    name: 'Search',
    components: {
        YipNetLayout,
        YipNetSearch
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
    }
}
</script>