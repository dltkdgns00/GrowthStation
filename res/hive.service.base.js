/**
 * @file hive.service.base.js
 * @brief .
 * @author       AnHive Co., Ltd. anhive@gmail.com
 * @date         2017~2023
**/

var POST = function (api, data, func)
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function ()
    {
        if (request.readyState == 4)
        {
            var resp = ""
            try
            {
                if (request.response[0] == '<')
                {
                    var resp = {
                        status: 'error',
                        data: 'Unknown error : ['
                            + request.responseText + ']'
                    };
                } else
                {
                    resp = JSON.parse(request.response);
                }
            } catch (e)
            {
                resp = {
                    status: 'error',
                    data: 'Unknown error : ['
                        + request.responseText + ']'
                };
                alert(request.responseText)
            }
            func(resp)
        }
    };
    request.open('POST', api);
    request.send(data);
    return request
}

var _ = function (id)
{
    return document.getElementById(id)
}
