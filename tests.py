import pytest, os, json
from app import app
from random import randint

pytest.main(args=['-s', os.path.abspath(__file__)])

index = randint(1000,10000)

def func():
    return True
class TestClass:
    def test_get_all_tasks(self):
        client = app.test_client(self)
        response = client.get('/api/todo/')
        assert response.status_code == 200
        res_body = json.loads(response.data)
        total_task = len(res_body)
        assert len(res_body) >= 1

    def test_get_one_tasks(self):
        client = app.test_client(self)
        response = client.get('/api/todo/?id=2')
        assert response.status_code == 200
        res_body = [json.loads(response.data)]
        assert len(res_body) == 1

    def test_can_create_new_task(self):
        client = app.test_client(self)        
        response = client.post('/api/todo/', 
            data=json.dumps({
            "id": index,
            "title": "my new test task",
            "completion_status": False
            }),
            content_type='application/json',
            )
        assert response.status_code == 200

    def test_cannot_create_duplicate_task(self):
        client = app.test_client(self)        
        response = client.post('/api/todo/', 
            data=json.dumps({
            "id": index,
            "title": "my new test task",
            "completion_status": False
            }),
            content_type='application/json',
            )
        assert response.status_code == 400
        assert 'Task Already Exists!' in str(response.data)

    def test_can_update_task_using_put(self):
        client = app.test_client(self)        
        response = client.put('/api/todo/?id={}'.format(index), 
            data=json.dumps({
            "id": index,
            "title": "my new updated test task using put",
            "completion_status": False
            }),
            content_type='application/json',
            )
        assert response.status_code == 200
        assert 'successful' in str(response.data)

    def test_can_update_task_using_patch(self):
        client = app.test_client(self)        
        response = client.patch('/api/todo/?id={}'.format(index), 
            data=json.dumps({
            "title": "my new updated test task using patch"
            }),
            content_type='application/json',
            )
        assert response.status_code == 200
        assert 'successful' in str(response.data)

    def test_cannot_update_no_task_using_patch(self):
        client = app.test_client(self)        
        response = client.patch('/api/todo/?id={}'.format(index*randint(2,5)), 
            data=json.dumps({
            "title": "X("
            }),
            content_type='application/json',
            )
        assert response.status_code == 400
        assert 'Unable to update task' in str(response.data)

    def test_can_delete_task(self):
        client = app.test_client(self)        
        response = client.delete('/api/todo/?id={}'.format(index))
        assert response.status_code == 200


    def test_cannot_delete_no_task(self):
        client = app.test_client(self)        
        response = client.delete('/api/todo/?id={}'.format(index*randint(2,5)))
        assert response.status_code == 400
        assert 'Task doesnot exist!' in str(response.data)

