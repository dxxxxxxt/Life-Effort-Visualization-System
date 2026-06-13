class CheckinManager {
    constructor() {
        this.todayCheckins = new Set();
    }

    async loadTodayCheckins() {
        try {
            const response = await fetch('/api/checkin/today');
            const data = await response.json();
            this.todayCheckins = new Set(data.checked_abilities);
            return data;
        } catch (error) {
            console.error('Failed to load today checkins:', error);
            return null;
        }
    }

    isChecked(abilityId) {
        return this.todayCheckins.has(abilityId);
    }

    async checkin(abilityId) {
        try {
            const response = await fetch('/api/checkin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ability_id: abilityId })
            });
            const data = await response.json();
            if (data.success) {
                this.todayCheckins.add(abilityId);
            }
            return data;
        } catch (error) {
            console.error('Checkin failed:', error);
            return { error: '网络错误' };
        }
    }
}

window.checkinManager = new CheckinManager();
