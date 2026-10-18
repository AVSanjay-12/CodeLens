export type DependencyStatus = {
    status: "available" | "unavailable";
};

export type ServiceHealth = {
    status: "ok" | "degraded";
    dependencies: {
        postgresql: DependencyStatus;
        redis: DependencyStatus;
        ollama: DependencyStatus;
    };
};

export async function fetchServiceHealth(): Promise<ServiceHealth> {
    const response = await fetch("/api/health");

    if (!response.ok && response.status !== 503) {
        throw new Error(`Health check failed with HTTP ${response.status}`);
    }

    return (await response.json()) as ServiceHealth;
}