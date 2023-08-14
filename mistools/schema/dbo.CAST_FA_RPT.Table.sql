DROP TABLE [dbo].[CAST_FA_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_FA_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_FA_RPT](
	[CAST_FA_RPT_ID] [bigint] NOT NULL,
	[CAST_FA_RPT_FLAG] [bit] NOT NULL,
	[CAST_FA_WORK_ID] [varchar](20) NULL,
	[CASTFA_COLLEGE_IDENTIFIER] [varchar](3) NULL,
	[CASTFA_TOS_TERM_IDENTIFIER] [varchar](3) NULL,
	[CASTFA_AWARD_AMOUNT] [varchar](5) NULL,
	[CASTFA_UNIQUE_KEY] [varchar](20) NULL,
	[CASTFA_REPORT_FLAG] [varchar](3) NULL,
	[CASTFA_REPORT_REASON] [varchar](10) NULL,
	[CAST_FA_WORK_ADDDATE] [datetime] NULL,
	[CAST_FA_WORK_ADDOPR] [varchar](20) NULL,
	[CAST_FA_WORK_CHGDATE] [datetime] NULL,
	[CAST_FA_WORK_CHGOPR] [varchar](20) NULL,
	[CASTFA_SB00_ID] [varchar](9) NULL
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_FA_R__CAST___7060BBD1]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_FA_RPT] ADD  DEFAULT ((1)) FOR [CAST_FA_RPT_FLAG]
END
GO