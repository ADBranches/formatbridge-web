// REST client for Actix-Web endpoints
export const apiClient = {
    getCase: async (id: string) => fetch(`/api/v1/cases/${id}`).then(res => res.json()),
};
