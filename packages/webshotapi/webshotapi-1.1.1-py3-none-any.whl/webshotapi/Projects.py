from gawsoft.api_client import Request, Response
from typing import List

class Projects:

    def __init__(self, client: Request):
        self.client = client

    def get_all(self, page=1) -> Response:
        """
        Get all projects

        :rtype: RESTResponse
        """
        return self.client.request('/projects','GET',{
            "page": page,
        })
    
    def get(self, id:int) -> Response:
        '''
        Return project data by id

        :param id:
        :return: RESTResponse
        '''
        return self.client.request(f'/projects/{id}','GET',{})

    def create(self, params:dict) -> Response:
        '''
        Create new project

        :param params: dict with data for new project
        :return: RESTResponse
        '''
        return self.client.request('/projects','POST',params)

    def remove(self, project_id:int) -> Response:
        '''
        Remove project by id

        :param project_id: project id
        :return: RESTResponse
        '''
        return self.client.request(f'/projects/{project_id}','DELETE',{})

    def update(self, id:int, data:dict) -> Response:
        '''
        Update existing project

        :param id: project id
        :param data: project data
        :return: RESTResponse
        '''
        return self.client.request(f'/projects/{id}','PATCH', data)

    def url_add(self, project_id:int, command: str, urls:List[str],params:dict) -> Response:
        '''
        Add url to download for selected project

        :param project_id: project_id
        :param urls: list with urls
        :param params: dict with parameters
        :return: RESTResponse
        '''
        return self.client.request(f'/projects/{project_id}/urls','POST',{
            'urls':urls,
            'command': command,
            'params':params
        })

    def url_delete(self,id:int,url_id:int) -> Response:
        '''
        Delete specific url for project

        :param id: project id
        :param url_id: link id
        :return: RESTResponse
        '''
        return self.client.request(f'/projects/{id}/urls/{url_id}','DELETE')

    def urls_get(self,id:int,page=1) -> Response:
        '''
        Get urls for project
        
        :param id: project id
        :param page: page number
        :return: RESTResponse
        '''
        return self.client.request(f'/projects/{id}/urls/?page={page}','GET',{})
