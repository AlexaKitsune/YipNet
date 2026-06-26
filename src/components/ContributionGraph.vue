<template>
    <UCard class="bg-black/20 border-0" variant="ghost">
        <h2 class="font-semibold mb-4">{{ $t('profile.activity') }}</h2>

        <div class="overflow-x-auto">
            <div class="min-w-max">
                <!-- meses -->
                <div class="ml-10 grid h-7 contribution-months">
                    <span
                        v-for="month in monthLabels"
                        :key="month.key"
                        class="text-xs opacity-60 self-start"
                        :style="{ gridColumn: `${month.week + 1} / span 4` }"
                    >
                        {{ month.label }}
                    </span>
                </div>

                <div class="flex gap-2">
                    <!-- días -->
                    <div class="grid grid-rows-7 gap-1 text-xs opacity-60">
                        <span></span>
                        <span>Mon</span>
                        <span></span>
                        <span>Wed</span>
                        <span></span>
                        <span>Fri</span>
                        <span></span>
                    </div>

                    <!-- grid -->
                    <div class="contribution-grid">
                        <div
                            v-for="day in gridDays"
                            :key="day.date"
                            class="size-3 rounded-sm"
                            :class="levelClass(day.total)"
                            :title="`${day.date}: ${day.total} activities`"
                        />
                    </div>
                </div>

                <!-- leyenda -->
                <div class="mt-3 ml-10 flex items-center gap-2 text-xs opacity-70">
                    <span>{{ $t('profile.less') }}</span>
                    <div class="size-3 rounded-sm bg-[#2a2a2a]" />
                    <div class="size-3 rounded-sm bg-[#2d104d]" />
                    <div class="size-3 rounded-sm bg-[#4a148c]" />
                    <div class="size-3 rounded-sm bg-[#7700ff]" />
                    <div class="size-3 rounded-sm bg-[#aa66ff]" />
                    <span>{{ $t('profile.more') }}</span>
                </div>
            </div>
        </div>
    </UCard>
</template>

<script>
export default {
    name: 'ContributionGraph',

    props: {
        contributions: {
            type: Array,
            default: () => []
        }
    },

    computed: {
        contributionMap() {
            return new Map(
                this.contributions.map(item => [
                    String(item.date).slice(0, 10),
                    Number(item.total || 0)
                ])
            )
        },

        gridDays() {
            const result = []
            const today = new Date()

            const start = new Date(today)
            start.setDate(today.getDate() - 364)

            const startDay = start.getDay()

            for (let i = 0; i < startDay; i++) {
                result.push({
                    date: `empty-start-${i}`,
                    total: 0,
                    empty: true
                })
            }

            for (let i = 0; i < 365; i++) {
                const date = new Date(start)
                date.setDate(start.getDate() + i)

                const key = date.toISOString().slice(0, 10)

                result.push({
                    date: key,
                    total: this.contributionMap.get(key) || 0,
                    empty: false
                })
            }

            return result
        },

        monthLabels() {
            const labels = []

            this.gridDays.forEach((day, index) => {
                if (day.empty) return

                const date = new Date(day.date)

                if (date.getDate() !== 1) return

                labels.push({
                    key: day.date,
                    week: Math.floor(index / 7),
                    label: date.toLocaleString('en', {
                        month: 'short'
                    })
                })
            })

            return labels
        }
    },

    methods: {
        levelClass(total) {
            if (total <= 0) return 'bg-[#2a2a2a]'
            if (total === 1) return 'bg-[#2d104d]'
            if (total <= 3) return 'bg-[#4a148c]'
            if (total <= 6) return 'bg-[#7700ff]'
            return 'bg-[#aa66ff]'
        }
    }
}
</script>

<style scoped>
.contribution-grid {
    display: grid;
    grid-auto-flow: column;
    grid-template-rows: repeat(7, 12px);
    gap: 4px;
}

.contribution-months {
    grid-template-columns: repeat(54, 16px);
}
</style>