# v2/src/api/services/scenario_service.py
from v2.src.api.api_routes.scenario_routes import ScenarioRoutes
from v2.src.api.factories.scenario_factory import ScenarioFactory
from v2.src.api.models.scenario import ScenarioData, ScenarioResponse
from v2.src.core.http.api_session import ApiSession


class ScenarioService:
    """Service for scenario CRUD operations"""

    def __init__(self, session: ApiSession):
        self.session = session

    def create_scenario(self, scenario_data: ScenarioData) -> ScenarioResponse:
        """Create new scenario via POST"""
        response = self.session.post(
            ScenarioRoutes.ADD_SCENARIO,
            data=scenario_data.model_dump(),  # Pydantic
        )
        assert response.status == 200, f'Failed to create scenario: {response.status}'
        return ScenarioResponse(**response.json())  # Parse into typed object

    def get_scenario(self, scenario_id: str) -> ScenarioResponse:
        """Get scenario by ID"""
        response = self.session.get(
            ScenarioRoutes.GET_SCENARIO, params={'id': scenario_id}
        )
        assert response.status == 200, f'Failed to get scenario: {response.status}'
        return ScenarioResponse(**response.json())  # Typed response

    def create_email_scenario(self, strategy_name: str, **kwargs) -> ScenarioResponse:
        """
        Create email scenario - strategy_name MUST come from test

        Args:
            strategy_name: Base name from test
            **kwargs: Optional overrides

        Returns:
            ScenarioResponse with scenario ID
        """
        scenario = ScenarioFactory.email_scenario(strategy_name=strategy_name, **kwargs)
        return self.create_scenario(scenario)
