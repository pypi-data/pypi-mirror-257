import pandas as pd
from typing import List, Union, Dict
from functools import lru_cache
from .constants import NetValueData
from .dataloader import BaseDataLoader
from gytoolkit import ppwdbapi
from gytoolkit.mailparser import MailClient
from gytoolkit.utils import load_netvalue, save_netvalue
from .utils import get_otc_nv, ppwnvformatter


class NetValueLoader(BaseDataLoader):
    """
    净值数据来源(按优先级):
        1-邮箱解析
        2-ppwdbapi
        3-otc
        4-本地手工净值
    """

    def __init__(self) -> None:
        self.mailapi = {}
        super().__init__(NetValueData)

    def set_mailapi(self, username, password):
        mailclient = MailClient(username=username, password=password)
        self.mailapi[username] = mailclient

    def update_local_mail(self, depth=50):
        if "mail" not in self.source.keys():
            raise ValueError("Please set local mail file first.")

        local_mail_file = self.source["mail"]
        mail_api = self.mailapi
        if len(mail_api) > 0:
            for mailaccount, api in mail_api.items():
                headers = api.get_mail_header(lookin_depth=depth)
                nv_list = api.parse_mails(headers)
                save_netvalue(nv_list, local_mail_file)
            self.load_mail.cache_clear()

    @lru_cache
    def load_mail(self):
        return load_netvalue(self.source["mail"], df=True)

    @lru_cache
    def load_local(self):
        return load_netvalue(self.source["local"], df=True)

    @lru_cache
    def load_otc(self):
        otc_folder = self.source["otc"]
        return get_otc_nv(otc_folder, df=True)

    def filter(
        self, nvdf: pd.DataFrame, reg_ids=None, start_date=None, end_date=None, **kwargs
    ):
        if nvdf.empty:
            return nvdf

        if reg_ids is not None:
            if isinstance(reg_ids, str):
                reg_ids = [reg_ids]
            nvdf = nvdf[nvdf.index.get_level_values("prodcode").isin(reg_ids)]
        if start_date:
            nvdf = nvdf[nvdf.index.get_level_values("date") >= start_date]
        if end_date:
            nvdf = nvdf[nvdf.index.get_level_values("date") <= end_date]

        return nvdf

    def load_ppw(
        self,
        reg_ids=None,
        ppw_ids=None,
        start_date=None,
        end_date=None,
        code_mapper: pd.Series = None,
    ):
        api: ppwdbapi = self.source["ppw"]

        if ppw_ids is None:
            ppw_ids = []
        if isinstance(ppw_ids, str):
            ppw_ids = [ppw_ids]

        if reg_ids is not None:
            if isinstance(reg_ids, str):
                reg_ids = [reg_ids]
            if isinstance(reg_ids, list):
                reg_ids = [reg_id for reg_id in reg_ids if reg_id is not None]
            fund_ids = api.get_fund(reg_ids=reg_ids).index.to_list()
            ppw_ids.extend(fund_ids)

            if code_mapper is not None:
                ppw_ids.extend(code_mapper[code_mapper.isin(reg_ids)].index.tolist())

        ppw_ids = list(set(ppw_ids))
        if len(ppw_ids) == 0 and reg_ids is None:
            ppw_ids = None
        raw_ppwnv = api.get_netvalue(ppw_ids, start_date, end_date)
        ppwnv = ppwnvformatter(raw_ppwnv, code_mapper=code_mapper, df=True)
        return ppwnv

    def load(
        self,
        reg_ids=None,
        ppw_ids=None,
        start_date=None,
        end_date=None,
        code_mapper=None,
        df=True,
    ) -> Union[List[NetValueData], pd.DataFrame]:
        return super().load(
            reg_ids=reg_ids,
            ppw_ids=ppw_ids,
            start_date=start_date,
            end_date=end_date,
            code_mapper=code_mapper,
            df=df,
        )

    # def set_local_otc(self, otc_folder_path):
    #     self.otc_folder_path = otc_folder_path
    #     self.get_local.cache_clear()

    # def set_addtional_file(self, additional_file):
    #     self.additional_file = additional_file
    #     self.get_local.cache_clear()
