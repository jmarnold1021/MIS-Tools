DROP TABLE [dbo].[CAST_SP_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_SP_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_SP_RPT](
	[CAST_SP_RPT_ID] [bigint] NOT NULL,
	[CAST_SP_RPT_FLAG] [bit] NOT NULL,
	[CAST_SP_WORK_ID] [varchar](10) NULL,
	[CAST_SP_WORK_ADDDATE] [datetime] NULL,
	[CAST_SP_WORK_ADDOPR] [varchar](20) NULL,
	[CAST_SP_WORK_CHGDATE] [datetime] NULL,
	[CAST_SP_WORK_CHGOPR] [varchar](20) NULL,
	[CASTSP_GI01] [varchar](3) NULL,
	[CASTSP_GI03] [varchar](3) NULL,
	[CASTSP_SB02] [varchar](3) NULL,
	[CASTSP_SB00] [varchar](9) NULL,
	[CASTSP_SP01] [varchar](6) NULL,
	[CASTSP_SP02] [varchar](1) NULL,
	[CASTSP_SP03] [datetime] NULL,
	[CASTSP_SP04] [varchar](5) NULL,
	[CASTSP_STUDENT_ID] [varchar](10) NULL,
	[CASTSP_KEY_IDX] [varchar](18) NULL,
	[CASTSP_ACAD_CREDENTIALS_ID] [varchar](10) NULL,
 CONSTRAINT [PK_SP_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_SP_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_SP_R__CAST___6F6108B5]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_SP_RPT] ADD  DEFAULT ((1)) FOR [CAST_SP_RPT_FLAG]
END
GO
