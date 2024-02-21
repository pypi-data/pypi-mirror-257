from hive.api import ApiManager, handling_single_page_methods, warning_wrong_parameters


class CostTreeResources(ApiManager):
    """Class that handles all the XAutomata cost_tree_resources APIs"""

    def cost_tree_resources(self, warm_start: bool = False,
        single_page: bool = False, page_size: int = 5000,
        kwargs: dict = None, **params) -> list:
        """Read Cost Tree Resources

        Args:
            warm_start (bool, optional): salva la risposta in un file e se viene richiamata la stessa funzione con gli stessi argomenti restituisce il contenuto del file. Default to False.
            single_page (bool, optional): se False la risposta viene ottenuta a step per non appesantire le API. Default to False.
            page_size (int, optional): Numero di oggetti per pagina se single_page == False. Default to 5000.
            kwargs (dict, optional): additional parameters for execute. Default to None.
            **params: additional parameters for the API.

        Keyword Args:
            sort_by (string optional): Stringa separata da virgole di campi su cui ordinare. Si indica uno o piu campi della risposta e si puo chiedere di ottenere i valori di quei campi in ordine ascendente o discendente. Esempio "Customer:Desc". Default to "". - parameter
            uuid_tree_node (string optional): additional filter - parameter
            uuid_tag (string optional): additional filter - parameter
            cost_category (string optional): additional filter - parameter
            cost_category_value (string optional): additional filter - parameter
            percentage (integer optional): additional filter - parameter
            null_fields (string optional): additional filter - parameter
            skip (integer optional): numero di oggetti che si vogliono saltare nella risposta. Default to 0. - parameter
            limit (integer optional): numero di oggetti massimi che si vogliono ottenere. Default to 1_000_000. - parameter
            like (boolean optional): Se True, eventuali filtri richiesti dalla API vengono presi come porzioni di testo, se False il matching sul campo dei filtri deve essere esatto. Default to True. - parameter
            join (boolean optional): Se join = true, ogni riga restituita conterra' chiavi aggiuntive che fanno riferimento ad altre entita', con cui la riga ha relazioni 1:1. Default to False - parameter
            count (boolean optional): Se True nel header della risposta e' presente la dimensione massima a db della chiamata fatta, sconsigliabile perche raddoppia il tempo per chiamata. Default to False. - parameter

        Returns: list"""
        if kwargs is None:
            kwargs = dict()
        official_params_list = ['sort_by', 'uuid_tree_node', 'uuid_tag',
            'cost_category', 'cost_category_value', 'percentage',
            'null_fields', 'skip', 'limit', 'like', 'join', 'count']
        params.get('sort_by'), params.get('uuid_tree_node'), params.get(
            'uuid_tag'), params.get('cost_category'), params.get(
            'cost_category_value'), params.get('percentage'), params.get(
            'null_fields'), params.get('skip'), params.get('limit'
            ), params.get('like'), params.get('join'), params.get('count')
        if not self._silence_warning:
            warning_wrong_parameters(self.cost_tree_resources.__name__,
                params, official_params_list)
        response = self.execute('GET', path=f'/cost_tree_resources/',
            single_page=single_page, page_size=page_size, warm_start=
            warm_start, params=params, **kwargs)
        return response

    def cost_tree_resources_create(self, kwargs: dict = None, **payload
        ) -> list:
        """Create Cost Tree Resource

        Args:
            kwargs (dict, optional): additional parameters for execute. Default to None.
            **payload: additional parameters for the API.

        Keyword Args:
            uuid_tree_node (string required): additional filter - payload
            cost_category (string required): additional filter - payload
            cost_category_value (string required): additional filter - payload
            percentage (integer optional): additional filter - payload

        Returns: list"""
        if kwargs is None:
            kwargs = dict()
        official_payload_list = ['uuid_tree_node', 'cost_category',
            'cost_category_value', 'percentage']
        payload.get('uuid_tree_node'), payload.get('cost_category'
            ), payload.get('cost_category_value'), payload.get('percentage')
        if not self._silence_warning:
            warning_wrong_parameters(self.cost_tree_resources_create.
                __name__, payload, official_payload_list)
        response = self.execute('POST', path=f'/cost_tree_resources/',
            payload=payload, **kwargs)
        return response

    def cost_tree_resources_uuid_tree_node(self, uuid_tree_node: str,
        uuid_tag: str, warm_start: bool = False, kwargs: dict = None, **params
        ) -> list:
        """Read Cost Tree Resources

        Args:
            uuid_tree_node (str, required): uuid_tree_node
            uuid_tag (str, required): uuid_tag
            warm_start (bool, optional): salva la risposta in un file e se viene richiamata la stessa funzione con gli stessi argomenti restituisce il contenuto del file. Default to False.
            kwargs (dict, optional): additional parameters for execute. Default to None.
            **params: additional parameters for the API.

        Keyword Args:
            join (boolean optional): Se join = true, ogni riga restituita conterra' chiavi aggiuntive che fanno riferimento ad altre entita', con cui la riga ha relazioni 1:1. Default to False - parameter

        Returns: list"""
        if kwargs is None:
            kwargs = dict()
        kwargs, params = handling_single_page_methods(kwargs=kwargs, params
            =params)
        official_params_list = ['join']
        params.get('join')
        if not self._silence_warning:
            warning_wrong_parameters(self.cost_tree_resources.__name__,
                params, official_params_list)
        response = self.execute('GET', path=
            f'/cost_tree_resources/{uuid_tree_node}/{uuid_tag}', warm_start
            =warm_start, params=params, **kwargs)
        return response

    def cost_tree_resources_put(self, uuid_tree_node: str, uuid_tag: str,
        kwargs: dict = None, **payload) -> list:
        """Update Cost Tree Resources

        Args:
            uuid_tree_node (str, required): uuid_tree_node
            uuid_tag (str, required): uuid_tag
            kwargs (dict, optional): additional parameters for execute. Default to None.
            **payload: additional parameters for the API.

        Keyword Args:
            uuid_tree_node (string optional): additional filter - payload
            cost_category (string optional): additional filter - payload
            cost_category_value (string optional): additional filter - payload
            percentage (integer optional): additional filter - payload

        Returns: list"""
        if kwargs is None:
            kwargs = dict()
        official_payload_list = ['uuid_tree_node', 'cost_category',
            'cost_category_value', 'percentage']
        payload.get('uuid_tree_node'), payload.get('cost_category'
            ), payload.get('cost_category_value'), payload.get('percentage')
        if not self._silence_warning:
            warning_wrong_parameters(self.cost_tree_resources_put.__name__,
                payload, official_payload_list)
        response = self.execute('PUT', path=
            f'/cost_tree_resources/{uuid_tree_node}/{uuid_tag}', payload=
            payload, **kwargs)
        return response

    def cost_tree_resources_delete(self, uuid_tree_node: str, uuid_tag: str,
        kwargs: dict = None) -> list:
        """Delete Cost Tree Resources

        Args:
            uuid_tree_node (str, required): uuid_tree_node
            uuid_tag (str, required): uuid_tag
            kwargs (dict, optional): additional parameters for execute. Default to None.

        Returns: list"""
        if kwargs is None:
            kwargs = dict()
        response = self.execute('DELETE', path=
            f'/cost_tree_resources/{uuid_tree_node}/{uuid_tag}', **kwargs)
        return response
