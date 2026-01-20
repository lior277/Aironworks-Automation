class ApiRoutes:

    # ---- Static ----
    post_create_campaign = "/http/users/campaigns"
    post_create_mgm_login = "/http/mgm/auth/login"

    # ---- Dynamic ----
    @staticmethod
    def get_timeline_details(user_id: int):
        return f"/http/users/{user_id}/trading-platform/timeline"

    @staticmethod
    def get_user_by_id(user_id: int):
        return f"/http/users/{user_id}"
